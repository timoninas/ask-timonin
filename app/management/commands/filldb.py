from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import *

from faker import Faker

faker = Faker('en_US')

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--comments', type=int)
        parser.add_argument('--votes', type=int)

    def handle(self, *args, **options):
        count_users = options['users']
        count_tags = options['tags']
        count_questions = options['questions']
        count_comments = options['comments']
        count_votes = options['votes']

        if count_users is not None:
            print(f"Users - {count_users}")
            self.generate_users(count_users)

        if count_tags is not None:
            print(f"Tags - {count_tags}")
            self.generate_tags(count_tags)

        if count_questions is not None:
            print(f"Questions - {count_questions}")
            self.generate_question(count_questions)

        if count_comments is not None:
            print(f"Comments - {count_comments}")
            self.generate_comments(count_comments)

        if count_votes is not None:
            print(f"Votes - {count_votes}")
            self.generate_votes(count_votes)

    def generate_users(self, count_users):
        users = []
        profiles = []
        for i in range(count_users):
            number = faker.pyint(min_value=0, max_value=5, step=1)
            username = faker.user_name()
            if number <= 3 and number > 0:
                username = faker.user_name() + str(faker.pyint(min_value=1902, max_value=2077, step=1))
            if number >= 3:
                username = faker.user_name() + '_' + faker.sentence().split(' ')[0]
            user = User(username=username, password=faker.password(), email=faker.email())
            users.append(user)
            profile = Profile(user=user, name=faker.name())
            profiles.append(profile)

            if len(users) >= 500 or len(profile) >= 500:
                Profile.objects.bulk_create(profiles)
                profiles.clear()
                User.objects.bulk_create(users)
                users.clear()
                print("Insert 500 users and profiles")

    def generate_tags(self, count_tags):
        created_tags = []
        tags = []

        for i in range(count_tags):
            tag = self.rangom_tag()
            if tag in created_tags:
                tag = self.rangom_tag()
            created_tags.append(tag)
            db_tag = Tag(title=tag)
            tags.append(db_tag)
            if (len(tags) >= 500):
                Tag.objects.bulk_create(tags)
                tags.clear()
                print("Insert 500 tags")

    def rangom_tag(self):
        tag = ""
        tag_len = faker.pyint(min_value=3, max_value=10, step=1)
        for j in range(tag_len):
            tag += faker.word()[0]
        if faker.pyint(min_value=0, max_value=10000, step=1) >= 9999:
            tag = faker.word()
        return tag

    def generate_question(self, count_questions):
        all_profile_ids = Profile.objects.values_list('id', flat=True)
        all_tag_ids = Tag.objects.values_list('id', flat=True)
        for i in range(count_questions):
            id_author = faker.pyint(min_value=0, max_value=all_profile_ids.count() - 1, step=1)
            question = Question(title=faker.sentence(),
                                text=faker.text(),
                                author_id=all_profile_ids[id_author])

            question.save()

            tags_count = faker.pyint(min_value=1, max_value=4, step=1)
            for j in range(tags_count):
                id_tag = faker.pyint(min_value=0, max_value=all_tag_ids.count() - 1, step=1)
                question.tags.add(all_tag_ids[id_tag])

            question.save()

            if (i % 500):
                print("Insert 500 questions")

    def generate_comments(self, count_comments):
        all_profile_ids = Profile.objects.values_list('id', flat=True)
        all_question_ids = Tag.objects.values_list('id', flat=True)
        comments = []
        for i in range(count_comments):
            id_author = faker.pyint(min_value=0, max_value=all_profile_ids.count() - 1, step=1)
            id_question = faker.pyint(min_value=0, max_value=all_question_ids.count() - 1, step=1)
            comment = Comment(text=faker.text(),
                                author_id=all_profile_ids[id_author],
                                question_id=all_question_ids[id_question])

            comments.append(comment)

            if len(comments) >= 500:
                Comment.objects.bulk_create(comments)
                comments.clear()
                print("Insert 500 comments")

    def generate_votes(self, count_votes):
        all_question_ids = Question.objects.values_list('id', flat=True)
        all_comment_ids = Comment.objects.values_list('id', flat=True)
        all_profile_ids = Profile.objects.values_list('id', flat=True)
        created_questions = []
        created_comments = []
        votes = []

        for i in range(count_votes):
            # generate like or dislike
            dis_or_not = 1
            if faker.pyint(min_value=0, max_value=2, step=1) == 0:
                dis_or_not = -1

            # generate profile
            profile_id = all_profile_ids[faker.pyint(min_value=0, max_value=all_profile_ids.count() - 1, step=1)]

            if faker.pyint(min_value=0, max_value=1, step=1) == 1:

                # add like or dislike for question

                # generate question
                question_id = all_question_ids[faker.pyint(min_value=0, max_value=all_question_ids.count() - 1, step=1)]
                question = Question.objects.get(id=question_id)

                # generate profile
                profile_id = all_profile_ids[faker.pyint(min_value=0, max_value=all_profile_ids.count() - 1, step=1)]

                current_vote = {}
                current_vote['question_id'] = question_id
                current_vote['profile_id'] = profile_id

                if current_vote not in created_questions:
                    created_questions.append(current_vote)
                    LikeDislike.objects.likeOrDislike(dis_or_not, profile_id, question_id, 0)
                    # votes.append(LikeDislike(content_object=question,
                    #                          value=dis_or_not,
                    #                          profile_id=profile_id))
            else:

                # add like or dislike for comment

                # generate question
                comment_id = all_comment_ids[faker.pyint(min_value=0, max_value=all_comment_ids.count() - 1, step=1)]
                comment = Comment.objects.get(id=comment_id)

                current_vote = {}
                current_vote['question_id'] = comment_id
                current_vote['profile_id'] = profile_id

                if current_vote not in created_comments:
                    created_comments.append(current_vote)
                    LikeDislike.objects.likeOrDislike(dis_or_not, profile_id, comment_id, 1)
                    # votes.append(LikeDislike(content_object=comment,
                    #                          value=dis_or_not,
                    #                          profile_id=profile_id))

            if len(votes) >= 500:
                LikeDislike.objects.bulk_create(votes)
                votes.clear()
                print("Insert 500 like-dislikes")
