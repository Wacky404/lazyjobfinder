from src.resume import Resume
from src.utils.logger import setup_logging
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
EDU = [{'Highscool Name': 'Some Achievements'},
       {'College', 'Degree and stuff'}]
P = {'cool thing': 'info on cool thing'}

# Faux pulled data from Job Description
JOB_LOC = '3923 S University Ave, Little Rock, AR 72204'
REQ_SKILLS = ['Python', 'Ruby', 'Cpp']
REQ_WRK_EXP = """3 Years experience in IT Help Desk position."""


class TestResume(unittest.TestCase):

    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()
