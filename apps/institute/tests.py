from django.test import TestCase
from .models import Institute, InstituteProgram
from ..program.models import Program, Level


class InstituteProgramThroughTest(TestCase):
    def setUp(self):
        # Create three institutes
        self.i1 = Institute.objects.create(name='I1', description='D1')
        self.i2 = Institute.objects.create(name='I2', description='D2')
        self.i3 = Institute.objects.create(name='I3', description='D3')

        level = Level.objects.create(name='level')

        # Create three programs:
        self.p1 = Program.objects.create(name='P1', description='D1', level=level)
        self.p2 = Program.objects.create(name='P2', description='D2', level=level)
        self.p3 = Program.objects.create(name='P3', description='D3', level=level)

        # i1 has all three programs
        InstituteProgram.objects.create(institute=self.i1, program=self.p1, fee=1)
        InstituteProgram.objects.create(institute=self.i1, program=self.p2, fee=2)
        InstituteProgram.objects.create(institute=self.i1, program=self.p3)

        # p2 is also in i1 and i2
        InstituteProgram.objects.create(institute=self.i2, program=self.p2, fee=2)
        InstituteProgram.objects.create(institute=self.i3, program=self.p2, fee=5)

    def test_unfiltered_relationship(self):
        p2_institutes = list(Institute.objects.filter(programs=self.p2).order_by('name'))
        self.assertEqual(p2_institutes, [self.i1, self.i2, self.i3])

    def test_extra_attribute(self):
        programs = Program.objects.filter(institute_program__fee=1)
        self.assertEqual(programs.count(), 1)
