# TODO: finish up last compares for AI to score
from typing import Optional, Set, Union, Dict, List, Tuple
from dataclasses import dataclass, field
from geopy.geocoders import Nominatim
from src.utils.logger import logger, setup_logging
from src.utils.helpers import is_float, parseStructuredResponse
from src.ai import ai_cmp
from src.prompts import Prompts
from src.algo import jaccard_similarity as js
from src.algo import haversine as hs
import math

# setup_logging()

N = Nominatim(user_agent="lazyjobfinder", timeout=5)
WEIGHTS: Dict[str, float] = {
    'location': 0.3,
    'skills': 0.35,
    'experience': 0.2,
    'education': 0.1,
    'projectAccuracy': 0.05
}
PROMPTS: Prompts = Prompts()


@dataclass
class Resume:
    """ Class to hold Resume data and calculate scores. """

    firstName: str
    middleName: Optional[str]
    lastName: str
    location: Optional[str]
    # miles; for now
    travelDistance: str
    email: Optional[str]
    summary: str
    workExp: str
    _ctx: Dict = field(default_factory=dict)
    geolocator = N
    coordinates: Tuple[float, ...] = field(default_factory=tuple)
    links: Dict = field(default_factory=dict)
    skills: Dict[str, str] = field(default_factory=dict)
    education: List[Dict] = field(default_factory=list)
    projects: Dict = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=lambda: WEIGHTS)
    scores: Dict[str, Optional[float]] = field(default_factory=lambda: {
        'skills':  None,
        'experience': None,
        'location': None,
        'education': None,
        'projectAccuracy': None,
        'overall': None,
    })

    def get_coordinates(self, location: Optional[str] = None) -> None:
        """
        Helper function to set location and get coordinates.

        Args:
            location: address of user, so we can pinpoint coordinates for distance finding. (string)

        Returns:
            Nothing.
        """
        if location is not None:
            self.location = location

        if isinstance(self.location, str):
            try:
                l = self.geolocator.geocode(self.location)
                coordinates: tuple[float, float] = (
                    l.latitude, l.longitude)
                self.coordinates = coordinates
            except Exception as e:
                self._ctx['get_coordinates'] = f"An exception of type {type(e).__name__} occurred. Details: {str(e)}"
                logger.exception(f"{self._ctx['get_coordinates']}")
                logger.debug('API call to set coordinates has errored.')

    def compareSkills(self, req_skills: list[str]) -> float:
        """
        Compare Resume Skills with Job Opportunity skills.

        Args:
            reqSkills: list of the required skills posted in the job listing (list[str])

        Returns:
            similarity value between 0 and 1; higher the better
        """
        score = js(set(self.skills.keys()), set(req_skills))
        self.scores['skills'] = score
        logger.info(
            f"{self.skills} has been compared to {req_skills}: score {score}")

        return score

    def compareLoc(self, job_location: str, units: str = "miles") -> Optional[float]:
        """
        Compare Location with Job Opportunity req. location; take into account
        user willingness to travel/distance calc.

        Args:
            jobLocation: standard U.S address format (string) ex: 123 Capital View, Little Rock, AR, US

        Returns:
            1 if distance to user is <= the threshold set by self.location,
            else returns negative value from 0 to 1 if distance exceeds threshold.
            Or returns None if there is an error witht the API call.
        """
        if self.travelDistance != 'remote':
            if is_float(self.travelDistance):
                try:
                    location = self.geolocator.geocode(job_location)
                except Exception as e:
                    self._ctx['compareLoc'] = f"An exception of type {type(e).__name__} occurred. Details: {str(e)}"
                    logger.exception(f"{self._ctx['compareLoc']}")
                    logger.debug(
                        f'API call to get coordinates {job_location} has errored.')
                    return None

                logger.debug(
                    f"{self.coordinates} derived from {self.location}")
                distance = hs(units=units, lat1=self.coordinates[0], lon1=self.coordinates[1],
                              lat2=location.latitude, lon2=location.longitude)
                # if the distance is exceeding the threshold, then we calculate the percent diff and make it neg to normalize later
                score = 1.0 if distance <= float(self.travelDistance) else -(abs(distance - float(
                    self.travelDistance)) / ((distance + float(self.travelDistance) / 2)))
                logger.info(
                    f"{self.coordinates} was compared to {location.latitude, location.longitude}: score {score}")
            else:
                return None
        else:
            score = 1.0
            logger.info(
                f"Distance wasn't measured because travelDistance is set to {self.travelDistance}")

        self.scores['location'] = score

        return score

    def compareWorkExp(self, rec_exp: str) -> Optional[float]:
        """
        Compare Work Experience with Job Opportunity req. experience. Done by LLM model.

        Args:
            rec_exp: recommended/required experience from job posting (list[string] or string)

        Returns:
            similarity score of user experience on resume to job posting rec/req experience (float)
        """
        try:
            response = ai_cmp(prompt=PROMPTS.prompt_cmp_work_exp(
                user_work_exp_fmted=self.workExp, job_desc_exp_fmted=rec_exp))
            logger.debug(response)
            structured_response: dict[str, str] = parseStructuredResponse(
                response=str(response))
            logger.debug(structured_response)

            if is_float(structured_response['score']):
                return float(structured_response['score'])

        except Exception as e:
            logger.exception(
                f"An exception of type {type(e).__name__} occurred. Details: {str(e)}")
            logger.debug(
                f'API call to compare {self.workExp} to {rec_exp} errored.')
            return None

        return None

    def compareEdu(self, req_edu: str | list[str]) -> Optional[float]:
        """
        Compare Education with Job Opportunity req. education. Done by LLM model.

        Args:
            req_edu: required/preferred education from job description (list[string] or string)

        Returns:
            similarity score between 0 and 1 of comparison (float)
        """
        try:
            response = ai_cmp(prompt=PROMPTS.prompt_cmp_edu(
                user_edu_fmted=self.education, job_desc_edu_fmted=req_edu))
            logger.debug(response)
            structured_response: dict[str, str] = parseStructuredResponse(
                response=str(response))
            logger.debug(structured_response)

            if is_float(structured_response['score']):
                return float(structured_response['score'])

        except Exception as e:
            logger.exception(
                f"An exception of type {type(e).__name__} occurred. Details: {str(e)}")
            logger.debug(
                f'API call to compare {self.workExp} to {rec_exp} errored.')
            return None

        return None

    def prjacc(self, job_position: str) -> Optional[float]:
        """
        Score for applicability of projects to Job Opportunity. Done by LLM model.

        Args:
            job_position: job title/position of job posting (list[string] or string)

        Returns:
            similarity score of projects compared to job title/position (float)
        """
        pass

    def score(self) -> float:
        """
        Overall Score of match with Job Opportunity. Higher the better.

        Returns:
            a float value representing the final score of master Resume against job post (float)
        """
        score: float = 0.0
        for key, val in self.scores.items():
            if val is not None:
                score += (val * self.weights[key])
            else:
                logger.warn(
                    f"There was score not calculated before final scoring!\n{self._ctx}")

        self.scores['overall'] = score
        logger.info(f"Overall score has been calculated at {score}")

        return score


if __name__ == '__main__':
    pass
