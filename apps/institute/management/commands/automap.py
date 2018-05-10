# -*- coding: utf-8 -*-
import datetime
from time import sleep
import sys

import re

from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from apps.institute.models import Institute, Personnel, Designation, InstitutePersonnel, ScholarshipCategory, \
    Award, Ranking, InstituteProgram, InstituteAward, Scholarship, Rank, InstituteDocument, InstituteImage, Admission
from apps.program.models import Faculty, Board, Discipline, Council, CouncilDocument, BoardDocument, BoardImage, Program


def get_set_value(obj, alchemy, arr):
    for attr in arr:
        value = getattr(alchemy, attr)
        setattr(obj, attr, value)
        obj.save()


def get_dict_key_form_value(value, dict):
    for key, val in dict.iteritems():
        if val == value or value in val:
            return key


def show_progress(percent):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('=' * (int(percent / 5)), percent))
    sys.stdout.flush()
    sleep(0.25)


class Command(BaseCommand):
    help = "Import from old db"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', default=None, type=str)
        parser.add_argument('db_name')
        parser.add_argument('host', default=None)
        parser.add_argument('--activity',
                            action='store_true',
                            dest='activity',
                            default=False,
                            help='Import User Detail')

    def handle(self, *args, **options):
        Base = automap_base()
        if options['password'] == 'None':
            options['password'] = ''
        host = options['host'] or 'localhost'
        engine = create_engine(
            'postgresql://' + options['username'] + ':' + options['password'] + '@' + host + '/' + options['db_name'])
        try:
            Base.prepare(engine, reflect=True)
        except:
            raise CommandError('Database ' + options['db_name'] + ':Not Found')

        session = Session(engine)

        try:
            _AbstractTitleSlug = Base.classes.college_abstracttitleslug
            _Brochure = Base.classes.college_brochure
            _Gallery = Base.classes.college_gallery
            _Designation = Base.classes.college_designation
            _Personnel = Base.classes.college_personnel
            _ScholarshipCategory = Base.classes.college_scholarshipcategory
            _Ranking = Base.classes.rank_ranking
            _Award = Base.classes.college_award
            _Faculty = Base.classes.college_faculty
            _University = Base.classes.college_university
            _CourseType = Base.classes.college_coursetype
            _Council = Base.classes.college_council
            _Course = Base.classes.college_course
            _College = Base.classes.college_college
            _Scholarship = Base.classes.college_scholarship
            _Rank = Base.classes.rank_rank
            _Admission = Base.classes.college_admission
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        abstract_title_slug = session.query(_AbstractTitleSlug)  # Mapping table
        designations = session.query(_Designation)  # Mapping table
        personnel = session.query(_Personnel)  # Mapping table
        scholarship_categories = session.query(_ScholarshipCategory)  # Mapping table
        rankings = session.query(_Ranking)  # Mapping table
        awards = session.query(_Award)  # Mapping table
        faculties = session.query(_Faculty)  # Mapping table
        universities = session.query(_University)  # Mapping table
        course_types = session.query(_CourseType)  # Mapping table
        councils = session.query(_Council)  # Mapping table
        brochures = session.query(_Brochure)  # Mapping table
        galleries = session.query(_Gallery)  # Mapping table
        courses = session.query(_Course)  # Mapping table
        colleges = session.query(_College)  # Mapping table
        scholarships = session.query(_Scholarship)  # Mapping table
        ranks = session.query(_Rank)  # Mapping table
        admissions = session.query(_Admission)  # Mapping table

        ##### Save Designation ###########

        self.stdout.write("Importing designations...")

        for designation in designations:
            _designation, designation_created = Designation.objects.get_or_create(
                previous_db_id=designation.id,
                name=designation.post,
            )
        self.stdout.write("Designation data imported")

        ###### Save Personnel ###########

        self.stdout.write("Importing personnel...")
        personnel_count = personnel.count()
        for cnt, person in enumerate(personnel):
            _person, person_created = Personnel.objects.get_or_create(
                previous_db_id=person.id,
                prefix=person.prefix,
                name=person.name,
                photo=person.photo,
            )
            percent = int(float(cnt) * 100 / personnel_count)
            show_progress(percent)

        self.stdout.write("Personnel imported")

        ###### Save Scholarship Category ###########

        self.stdout.write("Importing scholarship category...")
        for scholarship_category in scholarship_categories:
            _abstract_title_slug = abstract_title_slug.get(scholarship_category.abstracttitleslug_ptr_id)
            _scholarship_category, scholarship_category_created = ScholarshipCategory.objects.get_or_create(
                previous_db_id=_abstract_title_slug.id,
                name=_abstract_title_slug.title,
                slug=scholarship_category.slug,
            )
        self.stdout.write("Scholarship Category data imported")

        ##### Save Ranking ###########

        self.stdout.write("Importing ranking...")
        ranking_count = rankings.count()

        for cnt, ranking in enumerate(rankings):
            try:
                _ranking, _ranking_created = Ranking.objects.get_or_create(
                    previous_db_id=ranking.id,
                    name=ranking.title,
                    slug=ranking.slug,
                )
                _ranking.description = ranking.description
                _ranking.save()
            except IntegrityError as e:
                print(str(e) + ' ' + ranking.slug)
            percent = int(float(cnt) * 100 / ranking_count)
            show_progress(percent)
        self.stdout.write("Ranking imported")

        ###### Save Awards ###########

        self.stdout.write("Importing awards...")
        for award in awards:
            _award, award_created = Award.objects.get_or_create(
                previous_db_id=award.id,
                name=award.title,
                description=award.award
            )
        self.stdout.write("Award data imported")

        ###### Save Faculty ###########

        self.stdout.write("Importing faculties...")
        for faculty in faculties:
            _abstract_title_slug = abstract_title_slug.get(faculty.abstracttitleslug_ptr_id)
            _faculty, faculty_created = Faculty.objects.get_or_create(
                previous_db_id=_abstract_title_slug.id,
                name=_abstract_title_slug.title,
                slug=faculty.slug,
            )
        self.stdout.write("Faculty data imported")

        ##### Save Board ###########

        self.stdout.write("Importing boards...")
        university_count = universities.count()

        # ManyToMany relation holding table for university and faculty
        try:
            _UniversityFaculty = Base.classes.college_university_faculty
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        try:
            _UniversityCategory = Base.classes.college_university_category
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, university in enumerate(universities):
            category = [abstract_title_slug.get(uni_category.universitycategory_id) for uni_category in
                        session.query(_UniversityCategory).filter_by(university_id=university.id)]
            faculties = [Faculty.objects.get(previous_db_id=uni_faculty.faculty_id) for uni_faculty in
                         session.query(_UniversityFaculty).filter_by(university_id=university.id)]
            international = None
            if category:
                international = category[0].title in ['International University']
            established = None
            if university.established_on:
                established_match = re.search('\d+', university.established_on)
                established = int(established_match.group())
            try:
                _board, _board_created = Board.objects.get_or_create(
                    previous_db_id=university.id,
                    name=university.title,
                    slug=university.slug,
                    established=established,
                    phone=[university.phone],
                    email=[university.email],
                    international=international,
                )
                get_set_value(
                    _board,
                    university,
                    [
                        'short_name',
                        'address',
                        'logo',
                        'website',
                        'video_link',
                        'description',
                        'salient_features',
                    ])
                _board.faculties.add(*faculties)
                _board.save()
            except IntegrityError as e:
                print(str(e) + ' ' + university.slug)
            percent = int(float(cnt) * 100 / university_count)
            show_progress(percent)
        self.stdout.write("Board imported")

        ##### Save Board Document ###########

        self.stdout.write("Importing board documents...")

        try:
            _UniversityBrochure = Base.classes.college_university_brochure
            college_university_brochures = session.query(_UniversityBrochure)
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for college_university_brochure in college_university_brochures:
            brochure = brochures.get(college_university_brochure.brochure_id)
            board = Board.objects.get(previous_db_id=college_university_brochure.university_id)
            _board_document, board_document_created = BoardDocument.objects.get_or_create(
                name=brochure.title,
                board=board,
                file=brochure.brochure,
            )
        self.stdout.write("Board Brochures data imported")

        ##### Save Board Gallery ###########

        self.stdout.write("Importing board gallery...")

        try:
            _UniversityGallery = Base.classes.college_university_gallery
            college_university_galleries = session.query(_UniversityGallery)
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for college_university_gallery in college_university_galleries:
            gallery = galleries.get(college_university_gallery.gallery_id)
            board = Board.objects.get(previous_db_id=college_university_gallery.university_id)
            _board_image, board_image_created = BoardImage.objects.get_or_create(
                name=gallery.caption,
                board=board,
                file=gallery.image,
            )
        self.stdout.write("Board Brochures data imported")

        ##### Save Discipline ###########

        self.stdout.write("Importing discipline...")

        for course_type in course_types:
            _discipline, discipline_created = Discipline.objects.get_or_create(
                previous_db_id=course_type.id,
                name=course_type.title,
                slug=course_type.slug,
                full_name=course_type.full_name,
            )
        self.stdout.write("Discipline data imported")

        ##### Save Council ###########

        self.stdout.write("Importing councils...")

        for council in councils:
            _council, council_created = Council.objects.get_or_create(
                previous_db_id=council.id,
                name=council.title,
                slug=council.slug,
                short_name=council.short_name,
                address=council.address,
                logo=council.logo,
                email=council.email,
                phone=council.phone,
                website=council.website,
                description=council.description,
            )
        self.stdout.write("Council data imported")

        ##### Save Council Document ###########

        self.stdout.write("Importing councils documents...")

        try:
            _CouncilBrochure = Base.classes.college_council_brochure
            college_council_brochures = session.query(_CouncilBrochure)
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for college_university_brochure in college_council_brochures:
            brochure = brochures.get(college_university_brochure.brochure_id)
            council = Council.objects.get(previous_db_id=college_university_brochure.council_id)
            _council_document, council_document_created = CouncilDocument.objects.get_or_create(
                name=brochure.title,
                council=council,
                file=brochure.brochure,
            )
        self.stdout.write("Council Brochures data imported")

        ##### Save Course ###########

        self.stdout.write("Importing courses...")
        course_count = courses.count()
        try:
            # ManyToMany relation holding table for Course and Related Course
            _RelatedCourse = Base.classes.college_course_related_courses
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        try:
            _CourseCouncil = Base.classes.college_council_courses
            college_council_courses = session.query(_CourseCouncil)
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, course in enumerate(courses):
            course_level = None
            if course.level_id:
                course_level = abstract_title_slug.get(course.level_id)

            try:
                course_faculty = Faculty.objects.get(previous_db_id=course.faculty_id)
            except ObjectDoesNotExist:
                course_faculty = None

            try:
                course_council = college_council_courses.filter_by(course_id=course.id).first()
                council = None
                if course_council:
                    council = Council.objects.get(previous_db_id=course_council.council_id)
            except ObjectDoesNotExist:
                course_council = None

            try:
                discipline = Discipline.objects.get(previous_db_id=course.course_type_id)
            except ObjectDoesNotExist:
                discipline = None

            try:
                course_board = Board.objects.get(previous_db_id=course.university_id)
                board_name = course_board.name
            except ObjectDoesNotExist:
                course_board= None
                board_name = None

            try:
                _course, _course_created = Program.objects.get_or_create(
                    previous_db_id=course.id,
                    name=course.title,
                    slug=course.slug,
                    full_name=course.full_title,
                    level=course_level,
                    faculty=course_faculty,
                    board=course_board,
                    recognition=council,
                    job_prospects=course.job_prospectus,
                    featured=course.is_featured,
                    published=course.has_published,
                )
                get_set_value(
                    _course,
                    course,
                    [
                        'short_name',
                        'duration_years',
                        'duration_months',
                        'description',
                        'eligibility',
                        'salient_features',
                        'curricular_structure',
                        'admission_criteria',
                    ])
                if discipline:
                    disciplines= [discipline]
                    _course.disciplines.add(*disciplines)
                    _course.save()
            except IntegrityError as e:
                print(str(e) + course.slug)
            percent = int(float(cnt) * 100 / course_count)
            show_progress(percent)

        self.stdout.write("Setting related courses...")

        for cnt, course in enumerate(courses):
            related_courses = [Program.objects.get(previous_db_id=related_course.to_course_id) for related_course in
                               session.query(_RelatedCourse).filter_by(from_course_id=course.id)]
            try:
                _course = Program.objects.get(previous_db_id=course.id)
                _course.related_programs.add(*related_courses)
                _course.save()
            except IntegrityError as e:
                print(str(e) + course.slug)
            percent = int(float(cnt) * 100 / course_count)
            show_progress(percent)

        self.stdout.write("Course imported")

        ##### Save College ###########

        self.stdout.write("Importing college...")
        college_count = colleges.count()
        try:
            _CollegeUniversity = Base.classes.college_college_university
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        try:
            _CollegeDistrict = Base.classes.college_district
            college_districts = session.query(_CollegeDistrict)
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, college in enumerate(colleges):
            established = None
            if college.established:
                established_match = re.search('\d+', college.established)
                if established_match:
                    established = int(established_match.group())

            district = None
            if college.district_id:
                college_district = college_districts.get(college.district_id)
                district = college_district.name

            try:
                college_university = [Board.objects.get(previous_db_id=college_university.university_id) for
                                      college_university in
                                      session.query(_CollegeUniversity).filter_by(college_id=college.id)]
            except ObjectDoesNotExist:
                college_university = []

            try:
                _college, _college_created = Institute.objects.get_or_create(
                    previous_db_id=college.id,
                    name=college.title,
                    slug=college.slug,
                    established=established,
                    cover_image=college.cover_photo,
                    district=district,
                    phone=[college.phone],
                    email=[college.email],
                    ugc_accredition=college.has_ugc_accredition,
                    published=college.has_published,
                    verified=college.is_verified,
                    has_building=college.building_ownership,
                    has_land=college.land_ownership,
                    land=college.land_area,
                    class_capacity=college.class_size,
                )
                get_set_value(
                    _college,
                    college,
                    [
                        'short_name',
                        'code',
                        'logo',
                        'website',
                        'description',
                        'salient_features',
                        'admission_guidelines',
                        'scholarship_information',
                        'type',
                        'no_of_buildings',
                        'no_of_rooms',
                        'total_staffs',
                        'facebook',
                        'twitter',
                        'youtube',
                        'video_link',
                    ])
                _college.boards.add(*college_university)
                if college.latitude and college.longitude:
                    _college.point = Point(college.latitude, college.longitude)
                _college.save()
            except IntegrityError as e:
                print(str(e) + ' ' + college.slug)
            percent = int(float(cnt) * 100 / (college_count))
            show_progress(percent)

        self.stdout.write("Setting network colleges...")

        try:
            _NetworkCollege = Base.classes.college_college_network_colleges
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, college in enumerate(colleges):
            network_colleges = [Institute.objects.get(previous_db_id=network_college.to_college_id) for network_college
                                in
                                session.query(_NetworkCollege).filter_by(from_college_id=college.id)]
            try:
                _college = Institute.objects.get(previous_db_id=college.id)
                _college.network_institutes.add(*network_colleges)
                _college.save()
            except ObjectDoesNotExist as e:
                print(str(e) + college.slug)
            percent = int(float(cnt) * 100 / college_count)
            show_progress(percent)

        ##### Save Granular Course Details ###########

        try:
            _GranularCourseDetail = Base.classes.college_granularcoursedetails
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        granular_course_details = session.query(_GranularCourseDetail)  # Mapping table
        granular_count = granular_course_details.count()
        self.stdout.write("Setting granular course details...")
        for cnt, granular_course in enumerate(granular_course_details):
            try:
                institute = Institute.objects.get(previous_db_id=granular_course.college_id)
            except ObjectDoesNotExist:
                institute = None
            try:
                program = Program.objects.get(previous_db_id=granular_course.course_id)
            except ObjectDoesNotExist:
                program = None
            try:
                _institute_program, institute_program_created = InstituteProgram.objects.get_or_create(
                    program=program,
                    institute=institute,
                    year=granular_course.year,
                    fee=granular_course.total_fee,
                    seats=granular_course.seats,
                    time_slot=granular_course.timeslot,
                )
            except IntegrityError:
                print(str(e) + ' ' + granular_course.id)
            percent = int(float(cnt) * 100 / granular_count)
            show_progress(percent)

        ##### Save Institute Personnel Details ###########

        try:
            _CollegePersonnel = Base.classes.college_college_personnel
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        college_college_personnel = session.query(_CollegePersonnel)  # Mapping table
        college_personnel_count = college_college_personnel.count()
        self.stdout.write("Setting college personnel details...")
        for cnt, college_college_personnel in enumerate(college_college_personnel):
            try:
                institute = Institute.objects.get(previous_db_id=college_college_personnel.college_id)
            except ObjectDoesNotExist:
                continue

            try:
                institute_personnel = Personnel.objects.get(previous_db_id=college_college_personnel.personnel_id)
            except ObjectDoesNotExist:
                continue

            college_personnel = personnel.get(college_college_personnel.personnel_id)

            try:
                _institute_designation = Designation.objects.get(previous_db_id=college_personnel.designation_id)
            except ObjectDoesNotExist:
                continue

            try:
                _institute_personnel, institute_personnel_created = InstitutePersonnel.objects.get_or_create(
                    personnel=institute_personnel,
                    designation=_institute_designation,
                    institute=institute,
                    message=college_personnel.message,
                )
            except IntegrityError:
                print(str(e) + ' ' + granular_course.id)
            percent = int(float(cnt) * 100 / college_personnel_count)
            show_progress(percent)

        self.stdout.write("College personnel imported")


        ##### Save Institute Award Details ###########
        awards_count = awards.count()
        self.stdout.write("Setting college awards...")
        for cnt, college_award in enumerate(awards):
                try:
                    award = Award.objects.get(previous_db_id=college_award.id)
                except ObjectDoesNotExist:
                    continue

                try:
                    institute = Institute.objects.get(previous_db_id=college_award.college_id)
                except ObjectDoesNotExist:
                    continue

                position = None
                if college_award.position:
                    position_match = re.search('\d+', college_award.position)
                    if position_match:
                        position = int(position_match.group())

                try:
                    _institute_award, institute_award_created = InstituteAward.objects.get_or_create(
                        institute=institute,
                        award=award,
                        position=position,
                        year=college_award.year,
                        description=college_award.remarks,
                    )
                except IntegrityError:
                    print(str(e) + ' ' + granular_course.id)
                percent = int(float(cnt) * 100 / awards_count)
                show_progress(percent)

        self.stdout.write("College awards imported")
        self.stdout.write("College data imported")

        ###### Save Scholarship ###########

        self.stdout.write("Importing scholarship...")
        scholarship_count = scholarships.count()

        try:
            _CollegeScholarshipCategory = Base.classes.college_scholarship_category
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, scholarship in enumerate(scholarships):
            try:
                scholarship_categories = [
                    ScholarshipCategory.objects.get(previous_db_id=scholarship_category.scholarshipcategory_id)
                    for
                    scholarship_category in
                    session.query(_CollegeScholarshipCategory).filter_by(scholarship_id=scholarship.id)]
            except ObjectDoesNotExist:
                scholarship_categories = []

            if scholarship.college_id:
                try:
                    institute = Institute.objects.get(previous_db_id=scholarship.college_id)
                except ObjectDoesNotExist:
                    institute = None
            try:
                _scholarship, _scholarship_created = Scholarship.objects.get_or_create(
                    name=scholarship.title,
                    slug=scholarship.slug,
                    starts_on=scholarship.starts_on,
                    ends_on=scholarship.ends_on,
                    description=scholarship.description
                )
                institutes = [institute]
                _scholarship.categories.add(*scholarship_categories)
                _scholarship.institutes.add(*institutes)
                _scholarship.save()
            except IntegrityError as e:
                print(str(e) + ' ' + scholarship.slug)
            percent = int(float(cnt) * 100 / scholarship_count)
            show_progress(percent)
        self.stdout.write("Scholarship imported")

        ###### Save Rank ###########
        self.stdout.write("Importing ranking...")
        rank_count = ranks.count()

        for cnt, rank in enumerate(ranks):
            try:
                college = Institute.objects.get(previous_db_id=rank.college_id)
            except ObjectDoesNotExist:
                college = None

            try:
                ranking = Ranking.objects.get(previous_db_id=rank.ranking_id)
            except ObjectDoesNotExist:
                ranking = None

            try:
                _rank, _rank_created = Rank.objects.get_or_create(
                    rank=ranking,
                    position=rank.rank,
                    institute=institute,
                    size=rank.size,
                )
                _rank.created_on = rank.created_on
                _rank.save()
            except IntegrityError as e:
                print(str(e) + ' ' + str(rank.id))
            percent = int(float(cnt) * 100 / rank_count)
            show_progress(percent)
        self.stdout.write("Ranking imported")

        ###### Save College Document ###########

        self.stdout.write("Importing institute document...")
        institute_document_count = brochures.count()
        for cnt, brochure in enumerate(brochures):
            try:
                institute = Institute.objects.get(previous_db_id=brochure.college_id)
            except Exception as e:
                institute = None

            if institute:
                _institute_document, institute_document_created = InstituteDocument.objects.get_or_create(
                    institute=institute,
                    name=brochure.title,
                    file=brochure.brochure,
                )
            percent = int(float(cnt) * 100 / institute_document_count)
            show_progress(percent)

        self.stdout.write("Institute Document imported")

        ###### Save College Image ###########

        self.stdout.write("Importing institute image...")
        institute_image_count = galleries.count()
        for cnt, gallery in enumerate(galleries):
            try:
                institute = Institute.objects.get(previous_db_id=gallery.college_id)
            except Exception as e:
                institute = None
            print(institute)
            print(gallery.caption)
            print(gallery.image)
            if institute:
                _institute_image, institute_image_created = InstituteImage.objects.get_or_create(
                    name=gallery.caption,
                    institute=institute,
                    file=gallery.image,
                )


            percent = int(float(cnt) * 100 / institute_image_count)
            show_progress(percent)

        self.stdout.write("Institute Document imported")

        ###### Save Admission ###########

        self.stdout.write("Importing admission...")
        admission_count = admissions.count()

        try:
            _AdmissionCollege = Base.classes.college_admission_colleges
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        try:
            _AdmissionCourse = Base.classes.college_admission_courses
        except AttributeError as e:
            self.stdout.write("No table found named." + e[0])

        for cnt, admission in enumerate(admissions):

            try:
                admission_institutes = [Institute.objects.get(previous_db_id=admission_college.college_id)
                                     for
                                     admission_college in
                                     session.query(_AdmissionCollege).filter_by(admission_id=admission.id)]
            except ObjectDoesNotExist:
                admission_institutes = []

            try:
                admission_programs = [Program.objects.get(previous_db_id=admission_course.course_id)
                                     for
                                     admission_course in
                                     session.query(_AdmissionCourse).filter_by(admission_id=admission.id)]
            except ObjectDoesNotExist:
                admission_programs = []
            try:
                _admission, _admission_created = Admission.objects.get_or_create(
                    name=admission.title,
                    slug=admission.slug,
                    description=admission.description,
                    starts_on=admission.starts_on,
                    ends_on=admission.ends_on,
                )
                _admission.programs.add(*admission_programs)
                _admission.institutes.add(*admission_institutes)
                _admission.created_on = admission.created_on
                _admission.save()
            except IntegrityError as e:
                print(str(e) + ' ' + admission.slug)
            percent = int(float(cnt) * 100 / admission_count)
            show_progress(percent)
        self.stdout.write("Admission imported")

        self.stdout.write("Complete!")
        pass
