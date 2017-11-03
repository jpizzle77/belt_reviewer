from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User


class BookDBManager(models.Manager):
	def validate_info(self, request, data):
		print "inside the validate_info() method"

		errors=[]
	

		if len(data['title']) < 1: 
			errors.append(['title',"Book title cannot be empty."])

		if len(data['name']) < 1: 
			errors.append(['name',"Author cannot be empty."])

		if len(data['review']) < 1: 
			errors.append(['review',"Review cannot be empty."])

		if errors:
			return [False, errors]


		else:
			book_exist = Book.objects.filter(title = data['title']) #checking to see if book already exists in the DB
			if book_exist:
				errors.append([request,'This book already exists in the database'])
				print "the book has already been put in the database"
				return [False, errors]
			
			
			else:
				return [True]
		

	def create_book(self,request,data):
		print "inside the create_book() method"

		new_book = Book(title=data['title'])
		new_book.save()
		return new_book



class Book(models.Model):
	title = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = BookDBManager()
	def __repr__(self):
		return "<Title: {}>".format(self.title)

class AuthorDBManager(models.Manager):

	def create_author(self,request,data):
		print "inside the create_book() method"

		author = Author(name=data['name'])
		#print author.books.id 
		author.save()
		#print author.books.id, " <-----here's the authors.book id---------"
		return author


class Author(models.Model):
	name = models.CharField(max_length=255)
	
	books = models.ManyToManyField(Book, related_name = "authors")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AuthorDBManager()
	def __repr__(self):
		return "<Name: {}>".format(self.name)


class ReviewDBManager(models.Manager):

	def create_review(self,request,data):
		print "inside the create_review() method"

		review = Review(review=data['review'], user_id=data['user_id'],  rating=data['rating'])
		review.book_id = request.session["book_id"]
		print review.book_id, "<------------here's the book ID inside the create_review()-----------------"
		print review.rating, "<-------here's the rating-----------"
		print review.user_id, "<--user id--->"
		review.save()
		#note: review is an OBJECT. It will contain the book_id and the user_id as well as the review and rating.
		print "Review ID: ", review.id, "Review: ", review.review, "Book ID :", review.book_id, "User ID: ", review.user_id, "Review rating:", review.rating, "<----Loook here!!!"
		return review


class Review(models.Model):
	review = models.CharField(max_length=255, default ="shit fuck fuck shit")
	rating = models.IntegerField(default=1)
	user = models.ForeignKey(User, related_name = "user_reviews")
	book = models.ForeignKey(Book, related_name = "book_reviews")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ReviewDBManager()
	def __repr__(self):
		return "<Review: {}, Rating: {} >".format(self.review, self.rating)