-- 1. Find product and category of all products sold by someone living in Los Angeles.
SELECT p.product, pr.category
FROM purchase p
JOIN person s ON p.seller = s.name
JOIN product pr ON p.product = pr.name
WHERE s.city = 'Los Angeles';

-- 2. Find buyer who bought laptop (category = 'Laptop') but never bought cell phone (category = 'Cell').
SELECT DISTINCT p1.buyer
FROM purchase p1
JOIN product pr1 ON p1.product = pr1.name
WHERE pr1.category = 'laptop'
AND p1.buyer NOT IN (
    SELECT p2.buyer
    FROM purchase p2
    JOIN product pr2 ON p2.product = pr2.name
    WHERE pr2.category = 'cell'
);

-- 2. Alternative
-- SELECT DISTINCT p1.buyer
-- FROM purchase p1
-- JOIN product pr1 ON p1.product = pr1.name
-- WHERE pr1.category = 'Laptop'
-- EXCEPT
-- SELECT DISTINCT p2.buyer
-- FROM purchase p2
-- JOIN product pr2 ON p2.product = pr2.name
-- WHERE pr2.category = 'Cell';

-- 3. Find total sales amount of all products sold by people living in Los Angeles to someone living in San Diego.
SELECT SUM(p.price * p.qty) AS total_sales
FROM purchase p
JOIN person s ON p.seller = s.name
JOIN person b ON p.buyer = b.name
WHERE s.city = 'Los Angeles' AND b.city = 'San Diego';

-- 4. Find makers of products who make only one type (category) of products. Do not use aggregation for this query.
SELECT DISTINCT pr.maker
FROM product pr
WHERE NOT EXISTS (
    SELECT 1
    FROM product pr2
    WHERE pr.maker = pr2.maker
    AND pr.category <> pr2.category
);

-- 4. Alternative
-- WITH maker_categories AS (
--     SELECT DISTINCT maker, category
--     FROM product
-- )
-- SELECT maker
-- FROM maker_categories mc
-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM maker_categories mc2
--     WHERE mc.maker = mc2.maker
--     AND mc.category <> mc2.category
-- );

-- 5. Find categories of products that were sold the most (with the largest sales quantity). Note that there may be multiple such product categories.
SELECT category
FROM product
JOIN purchase ON product.name = purchase.product
GROUP BY category
HAVING SUM(qty) = (
    SELECT MAX(total_qty)
    FROM (
        SELECT SUM(qty) AS total_qty
        FROM product
        JOIN purchase ON product.name = purchase.product
        GROUP BY category
    ) AS subquery
);


-- 6. Find products which have at least 100 units sold. Return top 3 such products.
SELECT p.product, SUM(p.qty) AS total_qty
FROM purchase p
GROUP BY p.product
HAVING SUM(p.qty) >= 100
ORDER BY total_qty DESC
LIMIT 3;

-- 7. Using outer join, find products that have never been sold.
SELECT pr.name AS product
FROM product pr
LEFT JOIN purchase p ON pr.name = p.product
WHERE p.product IS NULL;
