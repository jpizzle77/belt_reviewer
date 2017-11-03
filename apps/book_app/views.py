from django.shortcuts import render, HttpResponse, redirect
from .. login_app.models import User
from models import Book, Author, Review
from django.contrib import messages

  # the index function is called when root is visited

def index(request):
	print "--------inside BOOK_APP INDEX route----------"
	

	context = {

		'books': Book.objects.all(),
		'reviews': Review.objects.all().order_by('-created_at')[:3]# grabbing the the last 3 reviews that were posted. Without the '-', it would have shown the first 3 reviews
	}
	
	return render(request, 'book_app/index.html', context)



def add(request):

	print "<------------------------inside book_app  ADD()-------------------------"
	if request.method == 'POST':
		print request.POST, "<-----here is the request.POST----------------------------"
		print request.POST['user_id'], "<-------------here is the user ID that is signed in------------"
		request.session['user_id']= request.POST['user_id']
		print request.session['user_id'],"<---------user_id stored into session!!!!!!!!!----------"
		book_id = Book.objects.last() #grabs the last id in DB to be used for the new book to be created
		print book_id.id, "<----------the last book_id------------------------------>"

		# calling the custom validate_info() method to validate the incoming data (first name, last name, email) is valid before being passed into DB. Will return either a True or False(with errors) response
		response = Book.objects.validate_info(request,request.POST)

		print response, '<----------here is the response (True or False (w a list of the errors returned as well))----------------'

		if response[0] == False: #this means the validations failed. Return back to the register page with the errors posted

			# returns the list of errors. 
			for message in response[1]:
				messages.error(request, message[1])
			return redirect('book_app:add')
		else:
				book = Book.objects.create_book(request,request.POST) # a new user is created via the custom create_user() method
				author = Author.objects.create_author(request,request.POST)
				print author.name, "<----authors name---------------------->"

				#a1.publications.add(p1)

				x= author.books.add(book)
				print "The X spot"

				request.session["book_id"]= book.id
				print request.session["book_id"],"<---here is the book ID right before going into the create_review()--------------"
				review = Review.objects.create_review(request,request.POST)
				print "#",review.id, review.review, "<------------------here is the review for the book------------>"
				print book, "<----------------what up new book !!!!!!!!!"
				print book.id, book.title
				
				request.session['book_id']= book.id
				number = book.id
				print number," <--------------here is the book ID!!!!!!!!!!!!!!!!!!!!!!"

				#return redirect('book_app: show', + book.id)
				return redirect('book_app:show', number = number)
	else:

		authors= Author.objects.values('name').distinct() #this will grab the author once. It wont show the same author over and over if inputted

		print authors, "<-------------heres the authors!!!!!!!!!!! Will only user the author name one time. So you could put in Steven King in with 5 different books, but only his name shows once"
		context = {

			"authors": authors
		}

		print context

		return render(request, 'book_app/add_book.html', context)


def review(request):
	print "---------------------inside the review()-------------------------------------"
	print request.POST
	print request.session['book_id'], "<====================book id in review()"
	review = Review.objects.create_review(request,request.POST)
	
	return redirect('book_app:show', request.session['book_id'])

def show(request,number):

	print number, "<-------------BOOK ID------------------>"
	request.session['book_id']= number
	print request.session['book_id'], "<====================book id in show"
	author = Author.objects.get(books__id=number)
	print author, "<-----------here is the Author-------------->"
	print author.name



	context = {
		'book': Book.objects.get(id =number),
		'author':author,
		'reviews':Review.objects.all(), 
		#'user': User.objects.get(id = request.session['user_id']),
		#'rating': Book.objects.get(id = number)

	}

	print context
	return render(request, 'book_app/show_book.html', context)

	

		

def clear(request):
	print '----------------            CLEARING THE SESSION         ---------------------'

	request.session.clear()

	return redirect('login_app:index')

