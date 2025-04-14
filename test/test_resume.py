from src.resume import Resume
from src.utils.logger import setup_logging, logger
import unittest
import os

setup_logging()

F = 'John'
M = 'A.'
L = 'Doe'
LOC = '2801 S University Ave, Little Rock, AR 72204'
TD = '50.0'
E = 'johndoe@gmail.com'
S = '''This is a short example summary.'''
WE = '''5 Years experince in IT Service Desk Postion.'''
LINKS = {'linkedin': 'https://linkedin.com/user'}
SKILLS = {'Python': '3 years experience', 'Cpp': '4 years experience'}
EDU = [
    {'Generic High School': 'Graduated with Honers. Seal for intro to IT.'},
    {'University of State': 'BS. Information Technology Minor in Applied Math'}
]
P = {
    'IT Asset Software': 'Local first IT software that can track IT assets and other information with sync to cloud, if wanted',
    'Stock Tracking': 'Built with CPP. This program allowed for quick integration of real-time stock information for applications.'
}

# Faux pulled data from Job Description
JOB_LOC = '3923 S University Ave, Little Rock, AR 72204'
REQ_SKILLS = ['Python', 'Ruby', 'Cpp']
REQ_WRK_EXP = """3 Years experience in IT Help Desk position."""
REQ_EDU = "BS. Computer Science or equivalent field, if no degree consumerate work experience can suffice."
JOB_POSITION = "Junior Developer"


class TestResume(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.T = Resume(firstName=F, middleName=M, lastName=L,
                        location=LOC, travelDistance=TD, email=E,
                        summary=S, workExp=WE, links=LINKS, skills=SKILLS,
                        education=EDU, projects=P)
        self.T.get_coordinates()

    def test_location(self):
        self.assertIsNotNone(
            self.T.location, msg=self.T._ctx)
        self.assertEqual(len(self.T.coordinates), 2, msg=self.T._ctx)

    def test_compareLocation(self):
        s = self.T.compareLoc(job_location=JOB_LOC)
        self.assertIs(type(s), float, msg=self.T._ctx)

    def test_compareskills(self):
        s = self.T.compareSkills(req_skills=REQ_SKILLS)
        self.assertIs(type(s), float)
        self.assertLessEqual(s, 1)
        self.assertGreaterEqual(s, 0)

    def test_compareWorkExp(self):
        s = self.T.compareWorkExp(rec_exp=REQ_WRK_EXP)
        self.assertIs(type(s), float)
        self.assertLessEqual(s, 1)
        self.assertGreaterEqual(s, 0)

    def test_compareEdu(self):
        s = self.T.compareEdu(req_edu=REQ_EDU)
        self.assertIs(type(s), float)
        self.assertLessEqual(s, 1)
        self.assertGreaterEqual(s, 0)

    def test_prjacc(self):
        s = self.T.prjacc(job_position=JOB_POSITION)
        self.assertIs(type(s), float)
        self.assertLessEqual(s, 1)
        self.assertGreaterEqual(s, 0)

    @classmethod
    def tearDownClass(self):
        s = self.T.score()
        # self.assertIs(type(s), float)
        # for k, v, in self.T.scores.items():
        #     self.assertIs(type(k), str)
        #     self.assertIs(type(v), float)
        logger.info(f"Testing of Resume score results:\n{self.T.scores}")


if __name__ == '__main__':
    unittest.main()
