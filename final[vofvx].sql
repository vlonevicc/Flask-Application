--Create a view named monthlyRentalSales that calculates monthly rental sales for all years of payments in the database. Order by year and month in ascending order.
CREATE VIEW monthlyRentalSales AS
select year(p.payment_date) as year, monthname(p.payment_date) as month, month(p.payment_date) as month_num, sum(p.amount) as TotalPayments
from payment p
group by year(p.payment_date), month(p.payment_date), monthname(p.payment_date)
order by year(p.payment_date), month(p.payment_date) asc; 

--Create a view named categoryTotals that calculates yearly rental sales for movie categories in the database. Order by year (ascending order) and name (descending order).
CREATE VIEW categoryTotals AS 
select year(p.payment_date) as year, c.name, sum(p.amount) as TotalPayments
from payment p
join rental r on p.rental_id = r.rental_id
join inventory i on r.inventory_id = i.inventory_id
join film f on i.film_id = f.film_id
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
group by year(p.payment_date), c.name
order by year(p.payment_date) asc, c.name asc;

--?numbers are off)Create a view named storeCitySales that calculates yearly rental sales for cities each rental store is located in. Order by year  in descending order.
CREATE VIEW storeCitySales AS
select ci.city, year(p.payment_date) as year, sum(p.amount) as TotalPayments
from payment p
join rental r on p.rental_id = r.rental_id
join inventory i on r.inventory_id = i.inventory_id
join store s on i.store_id = s.store_id
join address a on s.address_id = a.address_id
join city ci on a.city_id = ci.city_id
group by ci.city, year(p.payment_date)
order by year(p.payment_date) desc;

--Create a view named customerRentalSales that calculates yearly rental sales for each customer. Order by year (ascending) and TotalPayments in descending order.
CREATE VIEW customerRentalSales AS
select year(p.payment_date) as year, concat(c.first_name, ' ', c.last_name) as name, sum(p.amount) as TotalPayments 
from payment p
join customer c on p.customer_id = c.customer_id
group by year(p.payment_date), c.first_name, c.last_name
order by year(p.payment_date) asc, TotalPayments desc;

--?Create a view named customerMovieRentals that calculates yearly number of movies rented for each customer. Order by year (ascending) and TotalPayments in descending order. 
CREATE VIEW customerMovieRentals AS
select year(p.payment_date) as year, concat(c.first_name, ' ', c.last_name) as name, count(p.rental_id) as NumRentals
from payment p
join customer c on p.customer_id = c.customer_id
group by year(p.payment_date), c.first_name, c.last_name
order by year(p.payment_date) asc, NumRentals desc;

--Create a view named moviesPerCategory that calculates the number of movies in each category. Order by numMovies in descending order
CREATE VIEW moviesPerCategory AS
select c.name, count(f.film_id) as numMovies
from film f 
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
group by c.name
order by numMovies desc;

--Create a view named moviesPerCategoryInStock that calculates the number of movies in each category currently in inventory. Order by then number of movies in stock in descending order.
CREATE VIEW moviesPerCategoryInStock AS
select c.name, count(i.inventory_id) as InStock
from inventory i
join film f on i.film_id = f.film_id
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
group by c.name
order by InStock desc;

