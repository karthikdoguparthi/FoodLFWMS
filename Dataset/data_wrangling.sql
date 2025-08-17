
-- Step 1: Remove all non-digits
UPDATE providers_data
SET Contact = REGEXP_REPLACE(Contact, '[^0-9]', '');
UPDATE receivers_data
SET Contact = REGEXP_REPLACE(Contact, '[^0-9]', '');

-- Step 2: Remove leading zeros
UPDATE providers_data
SET Contact = REGEXP_REPLACE(Contact, '^0+', '');
UPDATE receivers_data
SET Contact = REGEXP_REPLACE(Contact, '^0+', '');

-- Step 3: Add leading 1 if missing
UPDATE providers_data
SET Contact = CONCAT('1', Contact)
WHERE Contact NOT LIKE '1%';
UPDATE receivers_data
SET Contact = CONCAT('1', Contact)
WHERE Contact NOT LIKE '1%';

-- Step 4: Format as US number (1XXX) XXX-XXXX
UPDATE providers_data
SET Contact = CONCAT(
    '(', SUBSTRING(Contact, 2, 3), ') ',
    SUBSTRING(Contact, 5, 3), '-',
    SUBSTRING(Contact, 8, 4)
)
WHERE LENGTH(Contact) = 11 AND Contact LIKE '1%';

UPDATE receivers_data
SET Contact = CONCAT(
    '(', SUBSTRING(Contact, 2, 3), ') ',
    SUBSTRING(Contact, 5, 3), '-',
    SUBSTRING(Contact, 8, 4)
)
WHERE LENGTH(Contact) = 11 AND Contact LIKE '1%';

-- Keep only leading 1 + next 10 digits
UPDATE providers_data
SET Contact = CONCAT(
    '+1',
    SUBSTRING(REGEXP_REPLACE(Contact, '[^0-9]', ''), 2, 10)
);


-- Format into +1 (XXX) XXX-XXXX
UPDATE providers_data
SET Contact = CONCAT(
    '+1 (', SUBSTRING(Contact, 3, 3), ') ',
    SUBSTRING(Contact, 6, 3), '-',
    SUBSTRING(Contact, 9, 4)
)
WHERE LENGTH(Contact) = 12 AND Contact LIKE '+1%';


-- Keep only leading 1 + next 10 digits
UPDATE receivers_data
SET Contact = CONCAT(
    '+1',
    SUBSTRING(REGEXP_REPLACE(Contact, '[^0-9]', ''), 2, 10)
);

-- Format into +1 (XXX) XXX-XXXX
UPDATE receivers_data
SET Contact = CONCAT(
    '+1 (', SUBSTRING(Contact, 3, 3), ') ',
    SUBSTRING(Contact, 6, 3), '-',
    SUBSTRING(Contact, 9, 4)
)
WHERE LENGTH(Contact) = 12 AND Contact LIKE '+1%';

-- Step 5: Clean and format names
  UPDATE providers_data 
  SET 
  Name = CONCAT(UPPER(LEFT(TRIM(REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(Name, ' +', ' '), '_', ' '), '-', ' '), '.', ' ')), 1)),
  LOWER(SUBSTRING(TRIM(REPLACE(REPLACE(REPLACE(REGEXP_REPLACE(Name, ' +', ' '), '_', ' '), '-', ' '), '.', ' ')), 2)));


-- Step 6: Clean food_listing_data food_type
UPDATE food_listings_data
SET Food_Type = CASE
    WHEN Food_Name IN ('Bread','Rice','Pasta','Salad','Vegetables','Dairy') THEN 'Vegetarian'
    WHEN Food_Name IN ('Chicken','Fish','Soup') THEN 'Non-Vegetarian'
    WHEN Food_Name = 'Fruits' THEN 'Vegan'
    ELSE 'Unknown'
END;
