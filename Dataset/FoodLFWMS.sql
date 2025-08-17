
# 1 Total Providers count in each city
select City,
	count(Provider_ID) as Total_providers
from 
	providers_data
group by City
order by Total_providers desc;

# 2 Total Receivers count in each city
select City,
	count(Receiver_ID) as Total_receivers
from 
	receivers_data
group by City
order by Total_receivers desc;

# 3 Food provider contribution for distribution 
select 
    p.Type as Provider_Type,
    count(f.Quantity) as Total_Quantity
from 
	providers_data p
join 
	food_listings_data f 
on 
	p.Provider_ID = f.Provider_ID
group by p.Type
order by Total_Quantity desc;

# 4 First POC for food providers in each city
select p.Provider_ID, p.Type, p.City, p.Contact
from 
	providers_data p
join (
    select City, min(Provider_ID) as min_id
    from 
		providers_data
    group by City
) as x
on 
	p.City = x.City
and 
	p.Provider_ID = x.min_id
order by p.City;

# 5 Receivers who have claimed the most food
select 
    r.Receiver_ID,
    r.Name as Receiver_Name,
    count(f.Quantity) as Total_Claimed_Quantity
from 
	claims_data c
join 
	food_listings_data f 
on
	c.Food_ID = f.Food_ID
join 
	receivers_data r 
on 
	c.Receiver_ID = r.Receiver_ID
where c.Status = 'completed'  
group by r.Receiver_ID, r.Name
order by total_claimed_quantity desc;

# 6 Total quantity of food available from all providers
select 
	Provider_Type, Food_Type, 
    count(Quantity) as Available_Food_Quantity
from 
	food_listings_data
group by Provider_Type,Food_Type
order by Available_Food_Quantity desc;

# 7 Food listing providers by type of food
select 
	p.name as Provider_Name, 
	f.Food_Name as Listing_Name, 
count(f.Food_ID) as Listing_count
from 
	providers_data p 
join
	food_listings_data f
on
	p.Provider_ID = f.Provider_ID
group by Provider_Name, Listing_Name
order by Listing_count desc;

# 8 Top 10 food providers
select p.name as Provider_Name,  
	count(f.Food_ID) as Listing_count
from 
	providers_data p 
join
	food_listings_data f
on
	p.Provider_ID = f.Provider_ID
group by Provider_Name
order by Listing_count desc
limit 10;

# 9 Most commonly available Food type 
select Food_Type,Meal_Type, 
	count(Quantity) as Quantity
from 
	food_listings_data
group by Food_Type,Meal_Type
order by Quantity desc;

# 10 Food claims made for each food item
select f.Food_Name as Food_Name, 
	count(c.Claim_ID) as Food_claims
from 
	claims_data c
join
	food_listings_data f
on 
	c.Food_ID = f.Food_ID
group by Food_Name
order by Food_claims desc;

# 11 Provider with highest number of successful claims
select p.Name as Provider_Name, 
	count(c.Claim_ID) as Food_claims
from 
	claims_data c
join
	food_listings_data f
on 
	c.Food_ID = f.Food_ID
join
	providers_data p
on
	p.Provider_ID = f.Provider_ID
where c.Status='Completed'
group by  Provider_Name
order by Food_claims desc;


# 12 Provider with successful food category
select p.Name as Provider_Name, f.Food_Name as Food_Name, 
	count(c.Claim_ID) as Food_claims
from 
	claims_data c
join
	food_listings_data f
on 
	c.Food_ID = f.Food_ID
join
	providers_data p
on
	p.Provider_ID = f.Provider_ID
where c.Status='Completed'
group by Food_Name, Provider_Name
order by Food_claims desc;


# 13  Food claims percentage
select 
    Status as Claim_Status,
    count(*) AS Status_Count,
    round(count(*) * 100.0 / (select count(*) from claims_data), 2) AS Percentage
from claims_data
group by Claim_Status
order by percentage desc;

#14 Average quantity of food claimed by receiver
select r.Name as Receiver_Name, round(avg(f.Quantity),2) as Quantity_Claimed
from receivers_data r 
join
	claims_data c
on
	r.Receiver_ID = c.Receiver_ID
join 
	food_listings_data f
on 
	f.Food_ID = c.Food_ID
where c.Status = 'Completed'
group by Receiver_Name
order by Quantity_Claimed desc;

# 15 Status count of Meal_Type
select 
	f.Meal_Type, c.Status as Status,
    count(c.Status) as Meal_count
from 
	food_listings_data f
join
	claims_data c
on
	f.Food_ID = c.Food_ID
group by f.Meal_Type, Status 
order by Status, Meal_count desc;

# 16 Most claimed Meal_type
select 
	f.Meal_Type, c.Status as Status,
    count(c.Status) as Meal_count
from 
	food_listings_data f
join
	claims_data c
on
	f.Food_ID = c.Food_ID
where c.Status = 'Completed'
group by f.Meal_Type, Status 
order by Status, Meal_count desc;

# 17 Quantity of food donated by each providedproviders_data
select
	p.Name as Provider_Name,
	sum(f.Quantity) as Quantity
from
	providers_data p 
join 
	food_listings_data f
on 
	p.Provider_ID = f.Provider_ID
group by Provider_Name
order by Quantity desc;

# 18 Quantity of food donated by each provided by food_type
select
	p.Name as Provider_Name,
    f.Food_Type as Food_type,
	sum(f.Quantity) as Quantity
from
	providers_data p 
join 
	food_listings_data f
on 
	p.Provider_ID = f.Provider_ID
group by Provider_Name,Food_type
order by Quantity desc;

#19 Food Wastage in each city
select 
    p.City,
    sum(f.Quantity) AS Wasted_Quantity
from providers_data p
join food_listings_data f
    on p.Provider_ID = f.Provider_ID
left join claims_data c
    on f.Food_ID = c.Food_ID 
   and c.Status = 'Completed'
where c.Food_ID IS null
group by p.City
order by wasted_quantity desc;

select * from providers_data;
select * from receivers_data;
select * from food_listings_data;
select * from claims_data;
