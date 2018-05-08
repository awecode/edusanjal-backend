# -*- coding: utf-8 -*-
import datetime
from time import sleep
import sys

import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from apps.institute.models import Institute, Personnel, Designation, InstitutePersonnel, ScholarshipCategory, \
    Award, Ranking
from apps.program.models import Faculty, Board


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
            _Designation = Base.classes.college_designation
            _Personnel = Base.classes.college_personnel
            _ScholarshipCategory = Base.classes.college_scholarshipcategory
            _Ranking = Base.classes.rank_ranking
            _Award = Base.classes.college_award
            _Faculty = Base.classes.college_faculty
            _University = Base.classes.college_university
            # _Level = Base.classes.course_level
            # _UniversityCategory = Base.classes.university_category
            # _CollegeCategory = Base.classes.college_category
            # _Type = Base.classes.college_type
            # _Author = Base.classes.blog_author
            # _NewsCategory = Base.classes.blog_category
            # _EventCategory = Base.classes.event_category
            # _Position = Base.classes.vacancy_position
            # _District = Base.classes.core_district
            # _Career = Base.classes.career_career
            # _Course = Base.classes.course_course
            # _College = Base.classes.college_college
            # _Advertisement = Base.classes.advertisement_advertisement
            # _Scholarship = Base.classes.scholarship_scholarship
            # _Admission = Base.classes.admission_admission
            # _Vacancy = Base.classes.vacancy_vacancy
            # _Event = Base.classes.event_event
            # _News = Base.classes.blog_blog
            # _Ranking = Base.classes.ranking_ranking
            # _Rank = Base.classes.ranking_rank
            # _Gallery = Base.classes.college_gallery
            # _Filer = Base.classes.filer_file
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
        #  levels = session.query(_Level)  # Mapping table
        # university_categories = session.query(_UniversityCategory)  # Mapping table
        # college_categories = session.query(_CollegeCategory)  # Mapping table
        # types = session.query(_Type)  # Mapping table
        # authors = session.query(_Author)  # Mapping table
        # news_categories = session.query(_NewsCategory)  # Mapping table
        # event_categories = session.query(_EventCategory)  # Mapping table
        # positions = session.query(_Position)  # Mapping table
        # districts = session.query(_District)  # Mapping table
        # careers = session.query(_Career)  # Mapping table
        # courses = session.query(_Course)  # Mapping table
        # colleges = session.query(_College)  # Mapping table
        # advertisements = session.query(_Advertisement)  # Mapping table
        # scholarships = session.query(_Scholarship)  # Mapping table
        # admissions = session.query(_Admission)  # Mapping table
        # vacancies = session.query(_Vacancy)  # Mapping table
        # events = session.query(_Event)  # Mapping table
        # news = session.query(_News)  # Mapping table

        # ranks = session.query(_Rank)  # Mapping table
        # galleries = session.query(_Gallery)  # Mapping table
        # filers = session.query(_Filer)  # Mapping table

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

        # self.stdout.write("University Category data imported")
        #
        # ###### Save College Category ###########
        # self.stdout.write("Importing college category...")
        # for college_category in college_categories:
        #     _college_category, college_category_created = CollegeCategory.objects.get_or_create(
        #         previous_db_id=college_category.id,
        #         title=college_category.title,
        #         slug=college_category.slug,
        #     )
        #     _college_category.created_on = college_category.created_on
        #     _college_category.save()
        #
        # self.stdout.write("College Category data imported")
        #
        # ###### Save Type ###########
        #
        # self.stdout.write("Importing type(ownership)...")
        # for type in types:
        #     _type, type_created = Type.objects.get_or_create(
        #         previous_db_id=type.id,
        #         title=type.title,
        #         slug=type.slug,
        #     )
        #     _type.created_on = type.created_on
        #     _type.save()
        #
        # self.stdout.write("Type data imported")
        #
        # ##### Save Author ###########
        #
        # self.stdout.write("Importing Author...")
        # for author in authors:
        #     _author, author_created = Author.objects.get_or_create(
        #         previous_db_id=author.id,
        #         title=author.title,
        #         slug=author.slug,
        #         email=author.email,
        #     )
        #     _author.created_on = author.created_on
        #     _author.save()
        #
        # self.stdout.write("Author data imported")
        #
        # ###### Save News Category ###########
        #
        # self.stdout.write("Importing news category...")
        # for news_category in news_categories:
        #     _news_category, news_category_created = NewsCategory.objects.get_or_create(
        #         previous_db_id=news_category.id,
        #         title=news_category.title,
        #         slug=news_category.slug,
        #     )
        #     _news_category.created_on = news_category.created_on
        #     _news_category.save()
        #
        # self.stdout.write("News Category data imported")
        #
        # ###### Save Event Category ###########
        #
        # self.stdout.write("Importing event category...")
        # for event_category in event_categories:
        #     _event_category, event_category_created = EventCategory.objects.get_or_create(
        #         previous_db_id=event_category.id,
        #         title=event_category.title,
        #         slug=event_category.slug,
        #     )
        #     _event_category.created_on = event_category.created_on
        #     _event_category.save()
        #
        # self.stdout.write("Event Category data imported")
        #
        # ###### Save Position ###########
        #
        # self.stdout.write("Importing position...")
        # for position in positions:
        #     _position, position_created = Position.objects.get_or_create(
        #         previous_db_id=position.id,
        #         title=position.title,
        #         slug=position.slug,
        #     )
        #     _position.created_on = position.created_on
        #     _position.save()
        #
        # self.stdout.write("Position data imported")
        #
        # ###### Save Distirct ###########
        #
        # self.stdout.write("Importing district...")
        # for district in districts:
        #     zone = Zone.objects.get(previous_db_id=district.zone_id)
        #     _district, district_created = District.objects.get_or_create(
        #         previous_db_id=district.id,
        #         name=district.name,
        #         slug=district.slug,
        #         zone=zone,
        #     )
        #
        # self.stdout.write("District imported")
        #
        #
        # ##### Save University ###########
        #
        # self.stdout.write("Importing university...")
        # university_count = universities.count()
        #
        # # ManyToMany relation holding table for university and faculty
        # try:
        #     _UniversityFaculty = Base.classes.university_university_faculty
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, university in enumerate(universities):
        #     uni_category = UniversityCategory.objects.get(previous_db_id=university.category_id)
        #     faculties = [Faculty.objects.get(previous_db_id=uni_faculty.faculty_id) for uni_faculty in
        #                  session.query(_UniversityFaculty).filter_by(university_id=university.id)]
        #     try:
        #         _university, _university_created = University.objects.get_or_create(
        #             previous_db_id=university.id,
        #             title=university.title,
        #             slug=university.slug,
        #             is_featured=university.featured,
        #             has_published=university.publish,
        #         )
        #         get_set_value(
        #             _university,
        #             university,
        #             [
        #                 'short_name',
        #                 'established_on',
        #                 'address',
        #                 'logo',
        #                 'phone',
        #                 'fax',
        #                 'email',
        #                 'website',
        #                 'latitude',
        #                 'longitude',
        #                 'description',
        #                 'salient_features',
        #             ])
        #         _university.faculty.add(*faculties)
        #         _university.category.add(uni_category)
        #         _university.created_on = university.created_on
        #         _university.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' +university.slug)
        #     percent = int(float(cnt) * 100 / university_count)
        #     show_progress(percent)
        # self.stdout.write("University imported")
        #
        #
        # ###### Save Career ###########
        #
        # self.stdout.write("Importing career...")
        # career_count = careers.count()
        #
        # for cnt, career in enumerate(careers):
        #
        #     try:
        #         faculty = Faculty.objects.get(previous_db_id=career.category_id)
        #     except ObjectDoesNotExist:
        #         faculty = None
        #
        #     _career, _career_created = Career.objects.get_or_create(
        #         previous_db_id=career.id,
        #         title=career.title,
        #         slug=career.slug,
        #         faculty=faculty,
        #         has_published=career.publish,
        #     )
        #     _career.description = career.description
        #     _career.created_on = career.created_on
        #     _career.save()
        #     percent = int(float(cnt) * 100 / career_count)
        #     show_progress(percent)
        #
        # self.stdout.write("Career imported")
        #
        #
        # ##### Save Course ###########
        #
        # self.stdout.write("Importing courses...")
        # course_count = courses.count()
        # try:
        #     # ManyToMany relation holding table for Course and Related Course
        #     _RelatedCourse = Base.classes.course_course_related_courses
        #     # ManyToMany relation holding table for Course and Career
        #     _CourseCareer = Base.classes.course_course_career
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, course in enumerate(courses):
        #     try:
        #         course_level = Level.objects.get(previous_db_id=course.level_id)
        #     except ObjectDoesNotExist:
        #         course_level = None
        #
        #     try:
        #         course_faculty = Faculty.objects.get(previous_db_id=course.faculty_id)
        #     except ObjectDoesNotExist:
        #         course_faculty = None
        #
        #     try:
        #         course_university = University.objects.get(previous_db_id=course.university_id)
        #         board_name = course_university.title
        #     except ObjectDoesNotExist:
        #         course_university = None
        #         board_name = None
        #     try:
        #        course_careers = [Career.objects.get(previous_db_id=course_career.career_id) for course_career in
        #                     session.query(_CourseCareer).filter_by(course_id=course.id)]
        #     except ObjectDoesNotExist:
        #         course_careers = []
        #
        #     try:
        #         _course, _course_created = Course.objects.get_or_create(
        #             previous_db_id=course.id,
        #             title=course.title,
        #             board_name=board_name,
        #             slug=course.slug,
        #             level=course_level,
        #             faculty=course_faculty,
        #             university=course_university,
        #             is_featured=course.featured,
        #             has_published=course.publish,
        #         )
        #         get_set_value(
        #             _course,
        #             course,
        #             [
        #                 'short_name',
        #                 'recognition',
        #                 'duration_years',
        #                 'duration_months',
        #                 'description',
        #                 'eligibility',
        #                 'job_prospectus',
        #                 'salient_features',
        #                 'curricular_structure',
        #                 'admission_criteria',
        #             ])
        #         _course.careers.add(*course_careers)
        #         _course.created_on = course.created_on
        #         _course.save()
        #     except IntegrityError as e:
        #         print(str(e) + course.slug)
        #     percent = int(float(cnt) * 100 / course_count)
        #     show_progress(percent)
        #
        #
        # self.stdout.write("Setting related courses...")
        #
        # for cnt, course in enumerate(courses):
        #     related_courses = [Course.objects.get(previous_db_id=related_course.to_course_id) for related_course in
        #                        session.query(_RelatedCourse).filter_by(from_course_id=course.id)]
        #     try:
        #         _course = Course.objects.get(previous_db_id=course.id)
        #         _course.related_courses.add(*related_courses)
        #         _course.save()
        #     except IntegrityError as e:
        #         print(str(e) + course.slug)
        #     percent = int(float(cnt) * 100 / course_count)
        #     show_progress(percent)
        #
        # self.stdout.write("Course imported")
        #
        #
        # ##### Save College ###########
        #
        # self.stdout.write("Importing college...")
        # college_count = colleges.count()
        # try:
        #     _CollegeUniversity = Base.classes.college_college_university
        #     _CollegePersonnel = Base.classes.college_college_personnel
        #     _CollegeCategory = Base.classes.college_college_category
        #     _NetworkCollege = Base.classes.college_college_network_colleges
        #
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, college in enumerate(colleges):
        #     try:
        #         college_district = District.objects.get(previous_db_id=college.district_id)
        #     except ObjectDoesNotExist:
        #         college_district = None
        #
        #     try:
        #         college_ownership = Type.objects.get(previous_db_id=college.type_id)
        #     except ObjectDoesNotExist:
        #         college_ownership = None
        #
        #     try:
        #         college_university = [University.objects.get(previous_db_id=college_university.university_id) for
        #                               college_university in
        #                               session.query(_CollegeUniversity).filter_by(college_id=college.id)]
        #     except ObjectDoesNotExist:
        #         college_university = []
        #
        #     try:
        #         college_personnel = [Personnel.objects.get(previous_db_id=college_personnel.personnel_id) for
        #                              college_personnel in
        #                              session.query(_CollegePersonnel).filter_by(college_id=college.id)]
        #     except ObjectDoesNotExist:
        #         college_personnel = []
        #
        #     try:
        #         college_category = [CollegeCategory.objects.get(previous_db_id=college_category.category_id) for
        #                             college_category in
        #                             session.query(_CollegeCategory).filter_by(college_id=college.id)]
        #     except ObjectDoesNotExist:
        #         college_category = []
        #
        #     try:
        #         _college, _college_created = College.objects.get_or_create(
        #             previous_db_id=college.id,
        #             title=college.title,
        #             slug=college.slug,
        #             district=college_district,
        #             is_featured=college.featured,
        #             has_published=college.publish,
        #             ownership_type=college_ownership,
        #             building_ownership=college.building_ownership,
        #             land_ownership=college.land_ownership,
        #             has_ugc_accredition=college.ugc_accredition,
        #         )
        #         get_set_value(
        #             _college,
        #             college,
        #             [
        #                 'established',
        #                 'short_name',
        #                 'logo',
        #                 'code',
        #                 'city',
        #                 'phone',
        #                 'fax',
        #                 'email',
        #                 'website',
        #                 'facebook',
        #                 'twitter',
        #                 'youtube',
        #                 'description',
        #                 'salient_features',
        #                 'admission_guidelines',
        #                 'scholarship_information',
        #                 'teaching_faculties',
        #                 'latitude',
        #                 'longitude',
        #                 'video_link',
        #                 'no_of_buildings',
        #                 'no_of_rooms',
        #                 'land_area',
        #                 'class_size',
        #             ])
        #         _college.university.add(*college_university)
        #         _college.personnel.add(*college_personnel)
        #         _college.category.add(*college_category)
        #         _college.created_on = college.created_on
        #         _college.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + college.slug)
        #     percent = int(float(cnt) * 100 / college_count)
        #     show_progress(percent)
        #
        # self.stdout.write("Setting network colleges...")
        #
        # for cnt, college in enumerate(colleges):
        #     related_colleges = [College.objects.get(previous_db_id=network_colleges.to_college_id) for network_colleges
        #                         in
        #                         session.query(_NetworkCollege).filter_by(from_college_id=college.id)]
        #     try:
        #         _college = College.objects.get(previous_db_id=college.id)
        #         _college.network_colleges.add(*related_colleges)
        #         _college.save()
        #     except ObjectDoesNotExist as e:
        #         print(str(e) + college.slug)
        #     percent = int(float(cnt) * 100 / college_count)
        #     show_progress(percent)
        #
        # ##### Save Granular Course Details ###########
        #
        # try:
        #     _GranularCourseDetail = Base.classes.college_granularcoursedetails
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # granular_course_details = session.query(_GranularCourseDetail)  # Mapping table
        # granular_count = granular_course_details.count()
        # self.stdout.write("Importing granular course details...")
        # for cnt, granular_course in enumerate(granular_course_details):
        #     try:
        #         college = College.objects.get(previous_db_id=granular_course.college_id)
        #     except ObjectDoesNotExist:
        #         college = None
        #     try:
        #         course = Course.objects.get(previous_db_id=granular_course.course_id)
        #     except ObjectDoesNotExist:
        #         course = None
        #     try:
        #         _granular_course, granular_course_created = GranularCourseDetails.objects.get_or_create(
        #             previous_db_id=granular_course.id,
        #             college=college,
        #             course=course,
        #             total_fee=granular_course.total_fee,
        #             seats=granular_course.seats,
        #             timeslot=granular_course.timeslot,
        #         )
        #         _granular_course.created_on = granular_course.created_on
        #         _granular_course.save()
        #     except IntegrityError:
        #         print(str(e) + ' ' + granular_course.id)
        #     percent = int(float(cnt) * 100 / granular_count)
        #     show_progress(percent)
        #
        # self.stdout.write("College data imported")
        #
        # ###### Save Advertisement ###########
        #
        # self.stdout.write("Importing advertisement...")
        # advertisement_count = advertisements.count()
        #
        # for cnt, advertisement in enumerate(advertisements):
        #     try:
        #         college = College.objects.get(previous_db_id=advertisement.college_id)
        #     except ObjectDoesNotExist:
        #         college = None
        #     _advertisement, _advertisement_created = Advertisement.objects.get_or_create(
        #         previous_db_id=advertisement.id,
        #         college=college,
        #         ad_image=advertisement.ad_image,
        #         position=advertisement.position,
        #         order=advertisement.order,
        #         url=advertisement.url,
        #         start_date=advertisement.start_date,
        #         end_date=advertisement.end_date,
        #         has_published=advertisement.publish,
        #     )
        #     _advertisement.created_on = advertisement.created_on
        #     _advertisement.save()
        #     percent = int(float(cnt) * 100 / advertisement_count)
        #     show_progress(percent)
        # self.stdout.write("Advertisement imported")
        #
        # ###### Save Scholarship ###########
        #
        # self.stdout.write("Importing scholarship...")
        # scholarship_count = scholarships.count()
        #
        # try:
        #     _ScholarshipScholarshipCategory = Base.classes.scholarship_scholarship_category
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, scholarship in enumerate(scholarships):
        #     try:
        #         scholarship_categories = [
        #             ScholarshipCategory.objects.get(previous_db_id=scholarship_category.category_id)
        #             for
        #             scholarship_category in
        #             session.query(_ScholarshipScholarshipCategory).filter_by(scholarship_id=scholarship.id)]
        #     except ObjectDoesNotExist:
        #         scholarship_categories = []
        #     try:
        #         _scholarship, _scholarship_created = Scholarship.objects.get_or_create(
        #             previous_db_id=scholarship.id,
        #             title=scholarship.title,
        #             slug=scholarship.slug,
        #             starts_on=scholarship.starts_on,
        #             ends_on=scholarship.ends_on,
        #             is_featured=scholarship.featured,
        #             has_published=scholarship.publish,
        #             is_pinned=scholarship.pinned,
        #         )
        #         _scholarship.description = scholarship.description
        #         _scholarship.category.add(*scholarship_categories)
        #         _scholarship.created_on = scholarship.created_on
        #         _scholarship.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + scholarship.slug)
        #     percent = int(float(cnt) * 100 / scholarship_count)
        #     show_progress(percent)
        # self.stdout.write("Scholarship imported")
        #
        # ###### Save Admission ###########
        #
        # self.stdout.write("Importing admission...")
        # admission_count = admissions.count()
        #
        # try:
        #     _AdmissionCourse = Base.classes.admission_admission_course
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, admission in enumerate(admissions):
        #     try:
        #         admission_university = University.objects.get(previous_db_id=admission.university_id) if admission.university_id else None
        #     except ObjectDoesNotExist:
        #         admission_university = None
        #
        #
        #     try:
        #         admission_colleges = [College.objects.get(previous_db_id=admission.college_id)] if admission.college_id else []
        #     except ObjectDoesNotExist:
        #         admission_colleges = []
        #
        #     try:
        #         admission_courses = [Course.objects.get(previous_db_id=admission_course.course_id)
        #                              for
        #                              admission_course in
        #                              session.query(_AdmissionCourse).filter_by(admission_id=admission.id)]
        #     except ObjectDoesNotExist:
        #         admission_courses = []
        #     try:
        #         _admission, _admission_created = Admission.objects.get_or_create(
        #             previous_db_id=admission.id,
        #             title=admission.title,
        #             slug=admission.slug,
        #             university=admission_university,
        #             starts_on=admission.starts_on,
        #             ends_on=admission.ends_on,
        #             is_featured=admission.featured,
        #             has_published=admission.publish,
        #         )
        #         _admission.description = admission.description
        #         _admission.courses.add(*admission_courses)
        #         _admission.colleges.add(*admission_colleges)
        #         _admission.created_on = admission.created_on
        #         _admission.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + admission.slug)
        #     percent = int(float(cnt) * 100 / admission_count)
        #     show_progress(percent)
        # self.stdout.write("Admission imported")
        #
        # ###### Save Vacancy ###########
        #
        # self.stdout.write("Importing vacancy...")
        # vacancy_count = vacancies.count()
        #
        # try:
        #     _VacancyPosition = Base.classes.vacancy_vacancy_position
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, vacancy in enumerate(vacancies):
        #     try:
        #         vacancy_university = University.objects.get(previous_db_id=vacancy.university_id) if vacancy.university_id else None
        #     except ObjectDoesNotExist:
        #         vacancy_university = None
        #     try:
        #         vacancy_college = College.objects.get(previous_db_id=vacancy.college_id) if vacancy.college_id else None
        #     except ObjectDoesNotExist:
        #         vacancy_college = None
        #
        #     try:
        #         vacancy_position = [Position.objects.get(previous_db_id=vacancy_position.position_id)
        #                             for
        #                             vacancy_position in
        #                             session.query(_VacancyPosition).filter_by(vacancy_id=vacancy.id)]
        #     except ObjectDoesNotExist:
        #         vacancy_position = []
        #     try:
        #         _vacancy, _vacancy_created = Vacancy.objects.get_or_create(
        #             previous_db_id=vacancy.id,
        #             title=vacancy.title,
        #             slug=vacancy.slug,
        #             university=vacancy_university,
        #             college=vacancy_college,
        #             job_type=vacancy.job_type,
        #             deadline=vacancy.deadline,
        #             salary=vacancy.salary,
        #             is_applicable=vacancy.application,
        #             is_featured=vacancy.featured,
        #             has_published=vacancy.publish,
        #         )
        #         _vacancy.description = vacancy.description
        #         _vacancy.position.add(*vacancy_position)
        #         _vacancy.created_on = vacancy.created_on
        #         _vacancy.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + vacancy.slug)
        #     percent = int(float(cnt) * 100 / vacancy_count)
        #     show_progress(percent)
        # self.stdout.write("Vacancy imported")
        #
        # ###### Save Event ###########
        #
        # self.stdout.write("Importing event...")
        # event_count = events.count()
        #
        # try:
        #     _EventEventCategory = Base.classes.event_event_category
        #     _EventParticipantCollege = Base.classes.event_event_participant_college
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, event in enumerate(events):
        #     try:
        #         event_categories = [EventCategory.objects.get(previous_db_id=event_category.category_id)
        #                             for
        #                             event_category in
        #                             session.query(_EventEventCategory).filter_by(event_id=event.id)]
        #     except ObjectDoesNotExist:
        #         event_categories = []
        #
        #     try:
        #         event_colleges = [College.objects.get(previous_db_id=event_college.college_id)
        #                           for
        #                           event_college in
        #                           session.query(_EventParticipantCollege).filter_by(event_id=event.id)]
        #     except ObjectDoesNotExist:
        #         event_colleges = []
        #     try:
        #         _event, _event_created = Event.objects.get_or_create(
        #             previous_db_id=event.id,
        #             title=event.title,
        #             slug=event.slug,
        #             starts_on=event.starts_on,
        #             ends_on=event.ends_on,
        #             venue=event.venue,
        #             phone=event.contact_phone,
        #             email=event.contact_email,
        #             website=event.contact_website,
        #             latitude=event.latitude,
        #             longitude=event.longitude,
        #             is_pinned=event.pinned,
        #             has_published=event.publish,
        #         )
        #         _event.description = event.description
        #         _event.category.add(*event_categories)
        #         _event.participant_college.add(*event_colleges)
        #         _event.created_on = event.created_on
        #         _event.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + event.slug)
        #     percent = int(float(cnt) * 100 / event_count)
        #     show_progress(percent)
        # self.stdout.write("Event imported")
        #
        # ###### Save News ###########
        #
        # self.stdout.write("Importing news...")
        # news_count = news.count()
        #
        # try:
        #     _NewsBlogCategory = Base.classes.blog_blog_category
        # except AttributeError as e:
        #     self.stdout.write("No table found named." + e[0])
        #
        # for cnt, obj in enumerate(news):
        #     try:
        #         news_author = Author.objects.get(previous_db_id=obj.author_id)
        #     except ObjectDoesNotExist:
        #         news_author = None
        #     try:
        #         news_categories = [NewsCategory.objects.get(previous_db_id=obj_category.category_id)
        #                            for
        #                            obj_category in
        #                            session.query(_NewsBlogCategory).filter_by(blog_id=obj.id)]
        #     except ObjectDoesNotExist:
        #         news_categories = []
        #     try:
        #         _obj, _obj_created = News.objects.get_or_create(
        #             previous_db_id=obj.id,
        #             title=obj.title,
        #             slug=obj.slug,
        #             author=news_author,
        #             is_pinned=obj.pinned,
        #             has_published=obj.publish,
        #         )
        #         _obj.description = obj.description
        #         _obj.category.add(*news_categories)
        #         _obj.created_on = obj.created_on
        #         _obj.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + obj.slug)
        #     percent = int(float(cnt) * 100 / news_count)
        #     show_progress(percent)
        # self.stdout.write("News imported")
        #
        # ###### Save Rank ###########
        # self.stdout.write("Importing ranking...")
        # rank_count = ranks.count()
        #
        # for cnt, rank in enumerate(ranks):
        #     try:
        #         college = College.objects.get(previous_db_id=rank.college_id)
        #     except ObjectDoesNotExist:
        #         college = None
        #
        #     try:
        #         ranking = Ranking.objects.get(previous_db_id=rank.ranking_id)
        #     except ObjectDoesNotExist:
        #         ranking = None
        #
        #     try:
        #         _rank, _rank_created = Rank.objects.get_or_create(
        #             previous_db_id=rank.id,
        #             ranking=ranking,
        #             college=college,
        #             rank=rank.rank,
        #             size=rank.size,
        #         )
        #         _rank.created_on = rank.created_on
        #         _rank.save()
        #     except IntegrityError as e:
        #         print(str(e) + ' ' + str(rank.id))
        #     percent = int(float(cnt) * 100 / rank_count)
        #     show_progress(percent)
        # self.stdout.write("Ranking imported")
        #
        # ##### Save Gallery ###########
        #
        # self.stdout.write("Importing gallery...")
        # gallery_count = galleries.count()
        #
        # for cnt, gallery in enumerate(galleries):
        #     try:
        #         gallery_college = College.objects.get(previous_db_id=gallery.college_id)
        #     except ObjectDoesNotExist:
        #         gallery_college = None
        #     if gallery_college:
        #         try:
        #             filer = session.query(_Filer).get(gallery.image_id)
        #         except ObjectDoesNotExist:
        #             filer = None
        #         try:
        #             _gallery, _gallery_created = Gallery.objects.get_or_create(
        #                 college=gallery_college,
        #                 image=filer.file,
        #                 caption=gallery.caption,
        #             )
        #         except Exception as e:
        #             print(str(e) + ' ' + str(gallery_college))
        #         percent = int(float(cnt) * 100 / gallery_count)
        #         show_progress(percent)
        # self.stdout.write("Gallery imported")
        #
        self.stdout.write("Complete!")
        pass
