from flask import render_template, redirect, url_for, request, flash, abort
from blueworks import app
from blueworks import app, db, bcrypt
from blueworks.forms import RegistrationForm_Company, RateCompanyForm, RegistrationForm_Consumer, AccountType, LoginForm, UpdateProfileConsumer, UpdateProfileCompany, SearchForm,PortfolioForm, ReviewForm
from blueworks.models import Company, Consumer, Portfolio, Review, Rating
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename
import tempfile
def save_picture_p(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path, quality=100)

    return picture_fn

def save_picture(form_picture, quality=90, max_width=300, max_height=300):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path, quality=100)

    return picture_fn

@app.route('/')
@app.route('/home')
def home():
    form = SearchForm()
    return render_template('home.html', form=form, title='Home')

@app.route('/account_type_signin', methods=['GET', 'POST'])
def account_type_signin():
    form = AccountType()
    
    if form.validate_on_submit():
        account_type = form.type.data

        if account_type == 'company':
            return redirect(url_for('register_company'))
        else:
            return redirect(url_for('register_consumer'))
    
    return render_template('account_type.html', form=form, title='Account Type Signin')

@app.route('/account_type_login', methods=['GET', 'POST'])
def account_type_login():
    form = AccountType()
    
    if form.validate_on_submit():
        account_type = form.type.data
        if account_type == 'company':
            return redirect(url_for('login_company'))
        else:
            return redirect(url_for('login_consumer'))
    
    return render_template('account_type.html', form=form, title='Account Type Login')

def generate_unique_id():
    # Start with ID 1
    new_id = 1
    while True:
        # Check if the ID exists in the Consumer table
        consumer_exists = Consumer.query.filter_by(id=new_id).first()

        # Check if the ID exists in the Company table
        company_exists = Company.query.filter_by(id=new_id).first()

        # If the ID is unique, return it
        if not consumer_exists and not company_exists:
            return new_id

        # Otherwise, increment the ID and try again
        new_id += 1

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm_Company()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Join the links while ignoring the empty ones
        all_links = ",".join([link_data['link'] for link_data in form.links.data if link_data['link']])
        
        # Generate a unique ID for the new company
        new_id = generate_unique_id()
        company = Company(
            links=all_links,
            id=new_id,
            phone=form.phone.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            location_country=form.location_country.data,
            location_province=form.location_province.data,
            location_city=form.location_city.data,
            address=form.address.data,
            company_type=form.company_type.data,
            licenses=form.licenses.data,
            bio=form.bio.data
        )
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('login_company'))
    print(form.errors)
    return render_template('register_company.html', form=form, title='Register Company')



@app.route('/register_consumer', methods=['GET', 'POST'])
def register_consumer():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm_Consumer()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Generate a unique ID for the new consumer
        new_id = generate_unique_id()

        consumer = Consumer(
            id=new_id,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            location_country=form.location_country.data,
            location_province=form.location_province.data,
            location_city=form.location_city.data,
            address=form.address.data
        )

        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('login_consumer'))
    return render_template('register_consumer.html', form=form, title='Register Cosumer')


@app.route('/login_company', methods=['POST', 'GET'])
def login_company():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(email=form.email.data).first()
        if company and bcrypt.check_password_hash(company.password, form.password.data):
            login_user(company, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login Company')

@app.route('/login_consumer', methods=['POST', 'GET'])
def login_consumer():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        consumer = Consumer.query.filter_by(email=form.email.data).first()
        if consumer and bcrypt.check_password_hash(consumer.password, form.password.data): 
            login_user(consumer, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login Consumer')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/about", methods=["GET", "POST"])
def about():
    form = SearchForm()
    return render_template('about.html', form=form)

@app.route("/profile_update_consumer", methods=["GET", "POST"])
@login_required
def profile_update_consumer():
    if (Consumer.query.get(current_user.id)) == None:
        return redirect('home')
    if Consumer.query.filter_by(username=current_user.username).first():  # Check if the current user is a consumer
        form = UpdateProfileConsumer()
        if form.validate_on_submit():
            if form.profile_picture.data:
                picture_file = save_picture(form.profile_picture.data)
                current_user.profile_picture = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.location_country = form.location_country.data
            current_user.location_province = form.location_province.data
            current_user.location_city = form.location_city.data
            current_user.address = form.address.data
            db.session.commit()
            return redirect('home')
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data =  current_user.email
            form.location_country.data = current_user.location_country
            form.location_province.data = current_user.location_province
            form.location_city.data = current_user.location_city
            form.address.data = current_user.address
        profile_picture = url_for('static', filename=current_user.profile_picture)
        consumer = current_user
        return render_template('profile_update_consumer.html', profile_picture=profile_picture, consumer=consumer, form=form, title='Profile Update Consumer')
    else:
        return redirect(url_for('profile_update_company'))


@app.route("/profile_update_company", methods=["GET", "POST"])
@login_required
def profile_update_company():
    
    # Check if user has a company profile
    company = Company.query.get(current_user.id)
    if not company:
        return redirect(url_for('home'))
    
    if Company.query.filter_by(username=current_user.username).first():
        form = UpdateProfileCompany()
        
        # POST request: form submission
        if form.validate_on_submit():
            if form.logo.data:
                picture_file = save_picture(form.logo.data)
                current_user.logo = picture_file
            
            current_links_list = current_user.links.split(',') if current_user.links else []

        # Handling deleted links
            existing_links_set = set(current_links_list)
            submitted_links_set = set([link_data['link'] for link_data in form.links.data if link_data['link']])
            
            # Identify new links and links to remove
            new_links = submitted_links_set - existing_links_set
            removed_links = existing_links_set - submitted_links_set
            
            # Add the new links and remove the old ones
            current_links_list = [link for link in current_links_list if link not in removed_links] + list(new_links)
            current_user.links = ','.join(current_links_list)

            
            # Updating other fields
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.location_country = form.location_country.data
            current_user.location_province = form.location_province.data
            current_user.location_city = form.location_city.data
            current_user.address = form.address.data
            current_user.company_type = form.company_type.data
            current_user.bio = form.bio.data
            current_user.licenses = form.licenses.data
            
            db.session.commit()
            
            return redirect(url_for('profile_company', username=current_user.username))
        
        # GET request: load form with current user data
        elif request.method == 'GET':
            existing_links = current_user.links.split(",") if current_user.links else []
            
            # Clearing out any existing form links data
            while len(form.links) > 0:
                form.links.pop_entry()
            
            # Filling form with user's existing links
            for link in existing_links:
                link_field = form.links.append_entry()
                link_field.link.data = link
            
            # Loading other user fields into form
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.phone.data = current_user.phone
            form.location_country.data = current_user.location_country
            form.location_province.data = current_user.location_province
            form.location_city.data = current_user.location_city
            form.address.data = current_user.address
            form.company_type.data = current_user.company_type
            form.bio.data = current_user.bio
            form.licenses.data = current_user.licenses
        
        # Return the form
        logo = url_for('static', filename=current_user.logo)
        company = current_user
        print(form.errors)
        return render_template('profile_update_company.html', title="Profile Update Company", logo=logo, company=company, form=form)
    else:
        # If user is not a company
        return redirect(url_for('profile_update_consumer'))



@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()    
    company = Company.query
    if form.validate_on_submit():
        search_term = form.searched.data.lower().strip()  # remove leading/trailing spaces
        if not search_term:  # if search_term is empty
            flash('Empty search term. Please enter a valid search term.')
            return redirect(request.referrer or url_for('home')) 

        companies = company.filter(
            (Company.username.ilike('%' + search_term + '%')) |
            (Company.location_city.ilike('%' + search_term + '%')) |
            (Company.company_type.ilike('%' + search_term + '%'))
        ).all()
        searched = form.searched.data
        return render_template("search.html", form=form, companies=companies, searched=searched, title='Search')
    else:
        flash('No results')
        return redirect(request.referrer or url_for('home')) 


# routes.py
@app.route('/profile/<string:username>/', methods=['POST', 'GET'])
def profile_company(username):
    form = SearchForm()
    rating_form = RateCompanyForm()
    company = Company.query.filter_by(username=username).first_or_404()
    review_form = ReviewForm()
    portfolios = Portfolio.query.filter_by(company_id=company.id).all()
    rating = Rating.query.filter_by(company_id=company.id)
    consumer = None
    if company.ratings_count == 0:  # Avoid dividing by zero.
        current_rating = 0
    else:
        current_rating = company.ratings
    if current_user.is_authenticated:
        if (Consumer.query.filter_by(id=current_user.id)) == None:
            consumer = None
        else:
            consumer = Consumer.query.get(current_user.id)
    return render_template('profile.html', title=f'Profile - {username}', company=company, portfolios=portfolios, form=form, review_form=review_form, rating=rating, current_rating=current_rating, rating_form=rating_form, consumer=consumer)





@app.route('/create_portfolio', methods=['GET', 'POST'])
@login_required
def create_portfolio():
    form = PortfolioForm()
    if Company.query.get(current_user.id) is None:
        flash('You need to create a company profile first!', 'warning')
        return redirect(url_for('home'))
    if form.validate_on_submit():
            company = Company.query.get(current_user.id)
            portfolio_data = {
                "company": company,
                "project_name": form.project_name.data,
                "description": form.description.data
            }
        
            # Handle multiple file uploads with a limit of 10 pictures
            for i in range(1, 11):  
                picture_field = getattr(form, 'picture_' + str(i))
                if picture_field.data:  
                    filename = save_picture(picture_field.data)
                    portfolio_data['picture_' + str(i)] = filename
                elif i == 1 and not portfolio_data.get('picture_1'):  # picture_1 is required
                    flash('The first picture is required!', 'danger')
                    return render_template('create_portfolio.html', form=form)

            portfolio = Portfolio(**portfolio_data)
            db.session.add(portfolio)
            db.session.commit()
            flash('Portfolio created successfully!', 'success')
            return redirect(url_for('profile_update_company'))

    return render_template('create_portfolio.html', form=form, title='Add Project')


@app.route("/portfolio/<int:portfolio_id>")
def portfolio(portfolio_id):
    form = SearchForm()
    review_form = ReviewForm()
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    pictures = [
        getattr(portfolio, f"picture_{i}") for i in range(1, 11) if getattr(portfolio, f"picture_{i}")
    ]
    return render_template(
        'project.html',
        portfolio=portfolio,
        pictures=pictures,
        form=form,
        review_form=review_form,
        title=f'Project - {portfolio.project_name}'
    )


@app.route("/portfolio/<int:portfolio_id>/delete", methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.company_id != current_user.id:   
        abort(403)
    db.session.delete(portfolio) 
    db.session.commit()
    
    return redirect(url_for('profile_company', username=current_user.username))

 

@app.route('/plumber_companies')
def plumber_companies():
    form = SearchForm()
    all_plumber_companies = Company.query.filter_by(company_type='plumber').all()
    plumber_companies = []
    city = ''
    province = ''
    if current_user.is_authenticated:
        for company in all_plumber_companies:
            if company.location_city == current_user.location_city and company.location_province == current_user.location_province:
                plumber_companies.append(company)
                city = company.location_city
                province = company.location_province
    else:
        plumber_companies = all_plumber_companies
    return render_template('companies.html', companies=plumber_companies, form=form, title=f'Plumbers {city} {province}')
@app.route('/electrician_companies')
def electrician_companies():
    form = SearchForm()
    all_electrician_companies = Company.query.filter_by(company_type='electrician').all()
    electrician_companies = []
    city = ''
    province = ''
    if current_user.is_authenticated:
        for company in all_electrician_companies:
            if company.location_city == current_user.location_city and company.location_province == current_user.location_province:
                electrician_companies.append(company)
                city = company.location_city
                province = company.location_province
    else:
        electrician_companies = all_electrician_companies
    return render_template('companies.html', companies=electrician_companies, form=form, title=f'Electricians {city} {province}')
@app.route('/carpenter_companies')
def carpenter_companies():
    form = SearchForm()
    all_carpenter_companies = Company.query.filter_by(company_type='carpenter').all()
    carpenter_companies = []
    city = ''
    province = None
    if current_user.is_authenticated:
        for company in all_carpenter_companies:
            if company.location_city == current_user.location_city and company.location_province == current_user.location_province:
                carpenter_companies.append(company)
                city = company.location_city
                province = company.location_province
    else:
        carpenter_companies = all_carpenter_companies
    return render_template('companies.html', companies=carpenter_companies, form=form, title=f'Carpenters {city} {province}')
@app.route('/handyman_companies')
def handyman_companies():
    form = SearchForm()
    all_handyman_companies = Company.query.filter_by(company_type='handyman').all()
    handyman_companies = []
    city = ''
    province = ''
    if current_user.is_authenticated:
        for company in all_handyman_companies:
            if company.location_city == current_user.location_city and company.location_province == current_user.location_province:
                handyman_companies.append(company)
                city = company.location_city
                province = company.location_province
    else:
        handyman_companies = all_handyman_companies

    return render_template('companies.html', companies=handyman_companies, form=form, title=f'Handyman {city} {province}')



@app.route("/create-review/<int:company_id>", methods=["POST"])
@login_required
def create_review(company_id):
    form = ReviewForm()
    if current_user.is_authenticated:
        company = Company.query.get(company_id)
        if not company:
            flash("Company not found!", "danger")
            return redirect(request.referrer)

        # Ensure that the current user is the company whose profile they're trying to write a review on.
        if not current_user.is_consumer and current_user.id != company_id:
            flash("You can only write a review on your own profile!", "danger")
            return redirect(request.referrer)

        if form.validate_on_submit():
            if current_user.is_consumer:
                review = Review(content=form.content.data, consumer_id=current_user.id, author_id=current_user.id, company_id=company_id)
            else: # Current user is a company
                review = Review(content=form.content.data, company_id=current_user.id, author_id=current_user.id)
                
            db.session.add(review)
            db.session.commit()

        return redirect(request.referrer)
    else:
        return redirect('account_type_signin')



@app.route("/delete-review/<int:review_id>")
@login_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        flash('Review does not exist.', category='error')
        return redirect(request.referrer)

    # Check if the current user wrote the review
    if current_user.id == review.author_id:
        db.session.delete(review)
        db.session.commit()
    else:
        flash('You do not have permission.', category='error')
    
    return redirect(request.referrer)





@app.route('/rate_company/<int:company_id>', methods=['GET', 'POST'])
@login_required
def rate_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        flash("Company not found", "danger")
        return redirect(url_for('home'))
    existing_rating = Rating.query.filter_by(company_id=company_id, consumer_id=current_user.id).first()
    if existing_rating:
        return redirect(url_for('profile_company', username=company.username))
    rating_form = RateCompanyForm()
    if rating_form.validate_on_submit():
        rating_value = rating_form.rating.data
        company.total_rating = (company.total_rating or 0) + rating_value  # Update the total_rating by adding the new rating_value
        company.ratings_count = (company.ratings_count or 0) + 1
        rating_average = company.total_rating / company.ratings_count
        rating_average = round(rating_average, 1)  # Round to 1 decimal place
        rating = Rating(company_id=company_id, consumer_id=current_user.id, rating=rating_average)
        db.session.add(rating)
        db.session.commit()
        return redirect(url_for('profile_company', username=company.username))
    else:
        return redirect(url_for('profile_company', username=company.username))

