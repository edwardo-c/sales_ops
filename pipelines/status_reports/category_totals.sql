-- tables: status_report_all_sales, status_report_customers

-- return yearly product category totals for customers only in status_report customers
-- return 0 if a customer does not have data for a specific category
WITH
    filtered_customers AS (
        SELECT
            s.acct_num,
            s.product_category,
            s.invoice_year,
            s.amount 
        FROM status_report_all_sales s
        INNER JOIN status_report_customers c
            ON c.acct_num = s.acct_num
    ),  
    categories AS (
        SELECT 'mount' as product_category
        UNION ALL SELECT 'tv'
        UNION ALL SELECT 'dvled'
        UNION ALL SELECT 'kiosk'
    ),
    all_combinations AS (
        SELECT DISTINCT
            fc.acct_num,
            cat.product_category,
            fc.invoice_year
            FROM (SELECT DISTINCT acct_num, invoice_year FROM filtered_customers) fc
        CROSS JOIN categories cat
    ) 
SELECT
    ac.acct_num,
    ac.product_category,
    ac.invoice_year,
    ROUND(COALESCE(SUM(fc.amount), 0), 2) AS CategoryTotal
FROM all_combinations ac
LEFT JOIN filtered_customers fc
    ON 
        ac.acct_num = fc.acct_num
        AND ac.product_category = fc.product_category
        AND ac.invoice_year = fc.invoice_year
GROUP BY ac.acct_num, ac.product_category, ac.invoice_year
ORDER BY ac.acct_num, ac.invoice_year, ac.product_category 



