
# Then we want to know the customer with a
# first name start with M who rented in store_id =1, what their rental histories?
# Please also order those histories by their address id.

use dvdrental;
select rental_id, customer.customer_id, first_name, last_name
from rental inner join customer on rental.customer_id = customer.customer_id
where customer.first_name Like 'M%' and customer.store_id = 1
order by customer.address_id;

select film_id, title
from film
where film_id in (select film_id from inventory
    where inventory.inventory_id in (select inventory_id from rental
        where return_date between timestamp '2005-05-29 00:00:00' AND timestamp '2005-05-30 23:59:59'));

# find out the actor (id,first_name,last_name) with most films.

# 1
select actor_id, count(*) AS cnt from film_actor
group by actor_id
order by cnt desc
limit 1;

select actor_id, first_name, last_name
from actor
where actor_id = 107;

# 2
select combine.actor_id, actor.actor_id, actor.first_name, actor.last_name
from actor inner join
(select actor_id, count(*) AS cnt from film_actor
group by actor_id) as combine on combine.actor_id = actor.actor_id
order by cnt desc
limit 1;

# find out the rental events for customer first/last name, phone, film title and return_date that
# returned before 2005-06-01.

# 1
select customer.first_name, customer.last_name, address.phone, rental.return_date, film.title
From address, customer, rental, film, inventory
where address.address_id = customer.address_id AND
      rental.customer_id = customer.customer_id AND
      rental.inventory_id = inventory.inventory_id AND
      inventory.film_id = film.film_id AND
      rental.return_date <= timestamp '2005-06-01 00:00:00';


# 2
select customer.first_name, customer.last_name, address.phone, rental.return_date, film.title
From address inner join customer on address.address_id = customer.address_id
inner join rental on rental.customer_id = customer.customer_id
inner join inventory on inventory.inventory_id = rental.inventory_id
inner join film on film.film_id = inventory.film_id
where rental.return_date <= timestamp '2005-06-01 00:00:00';

# Action 1
select film_id
from film
where length < 60 AND film_id IN (select film_id from film_category
    where film_category.category_id = (select category_id from category
        where name = 'Action'));

# Action 2
select film.film_id
from film, film_category, category
where film.film_id = film_category.film_id AND
      category.category_id = film_category.category_id AND
      film.length < 60 AND
      category.name = 'Action';

# get the films (id and title) that are not in the inventory, then order the results by title.
select film.film_id, film.title, inventory.film_id
from film left join inventory on film.film_id = inventory.film_id
where inventory.film_id is null
order by title;
