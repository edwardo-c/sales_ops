WITH filtered AS (
    SELECT
        s.acct_num,
        CASE
            WHEN LOWER(s.product_category) IN ('mount','mounts') THEN 'mounts'
            WHEN LOWER(s.product_category) IN ('tv','tech')       THEN 'tech'
            WHEN LOWER(s.product_category) IN ('kiosk','kiosks')  THEN 'kiosks'
            WHEN LOWER(s.product_category) = 'dvled'              THEN 'dvled'
            ELSE LOWER(s.product_category)
        END AS product_category,
        s.invoice_year,
        s.amount,
        c.header,
        c.timeframe,
        c.level_one_mount_goal,
        c.level_one_tech_goal,
        c.level_one_kiosks_goal,
        c.level_one_dvled_goal,
        c.level_one_mount_percent,
        c.level_one_tech_percent,
        c.level_one_kiosks_percent,
        c.level_one_dvled_percent,
        c.level_two_mount_goal,
        c.level_two_tech_goal,
        c.level_two_kiosks_goal,
        c.level_two_dvled_goal,
        c.level_two_mount_percent,
        c.level_two_tech_percent,
        c.level_two_kiosks_percent,
        c.level_two_dvled_percent,
        c.level_three_mount_goal,
        c.level_three_tech_goal,
        c.level_three_kiosks_goal,
        c.level_three_dvled_goal,
        c.level_three_mount_percent,
        c.level_three_tech_percent,
        c.level_three_kiosks_percent,
        c.level_three_dvled_percent
    FROM status_report_all_sales s
    INNER JOIN std_cat_customers c
        ON c.acct_num = s.acct_num
)
SELECT
    f.acct_num,
    MAX(f.header)      AS header,
    MAX(f.timeframe)   AS timeframe,
    MAX(f.level_one_mount_goal)      AS level_one_mount_goal,
    MAX(f.level_one_tech_goal)       AS level_one_tech_goal,
    MAX(f.level_one_kiosks_goal)     AS level_one_kiosks_goal,
    MAX(f.level_one_dvled_goal)      AS level_one_dvled_goal,
    MAX(f.level_one_mount_percent)   AS level_one_mount_percent,
    MAX(f.level_one_tech_percent)    AS level_one_tech_percent,
    MAX(f.level_one_kiosks_percent)  AS level_one_kiosks_percent,
    MAX(f.level_one_dvled_percent)   AS level_one_dvled_percent,
    MAX(f.level_two_mount_goal)      AS level_two_mount_goal,
    MAX(f.level_two_tech_goal)       AS level_two_tech_goal,
    MAX(f.level_two_kiosks_goal)     AS level_two_kiosks_goal,
    MAX(f.level_two_dvled_goal)      AS level_two_dvled_goal,
    MAX(f.level_two_mount_percent)   AS level_two_mount_percent,
    MAX(f.level_two_tech_percent)    AS level_two_tech_percent,
    MAX(f.level_two_kiosks_percent)  AS level_two_kiosks_percent,
    MAX(f.level_two_dvled_percent)   AS level_two_dvled_percent,
    MAX(f.level_three_mount_goal)    AS level_three_mount_goal,
    MAX(f.level_three_tech_goal)     AS level_three_tech_goal,
    MAX(f.level_three_kiosks_goal)   AS level_three_kiosks_goal,
    MAX(f.level_three_dvled_goal)    AS level_three_dvled_goal,
    MAX(f.level_three_mount_percent) AS level_three_mount_percent,
    MAX(f.level_three_tech_percent)  AS level_three_tech_percent,
    MAX(f.level_three_kiosks_percent)AS level_three_kiosks_percent,
    MAX(f.level_three_dvled_percent) AS level_three_dvled_percent,

    ISNULL(SUM(CASE WHEN invoice_year = :previous_year AND product_category='mounts' THEN amount END),0) AS previous_year_mounts,
    ISNULL(SUM(CASE WHEN invoice_year = :previous_year AND product_category='tech'   THEN amount END),0) AS previous_year_tech,
    ISNULL(SUM(CASE WHEN invoice_year = :previous_year AND product_category='kiosks' THEN amount END),0) AS previous_year_kiosks,
    ISNULL(SUM(CASE WHEN invoice_year = :previous_year AND product_category='dvled'  THEN amount END),0) AS previous_year_dvled,
    ISNULL(SUM(CASE WHEN invoice_year = :current_year  AND product_category='mounts' THEN amount END),0) AS current_year_mounts,
    ISNULL(SUM(CASE WHEN invoice_year = :current_year  AND product_category='tech'   THEN amount END),0) AS current_year_tech,
    ISNULL(SUM(CASE WHEN invoice_year = :current_year  AND product_category='kiosks' THEN amount END),0) AS current_year_kiosks,
    ISNULL(SUM(CASE WHEN invoice_year = :current_year  AND product_category='dvled'  THEN amount END),0) AS current_year_dvled
FROM filtered f
GROUP BY
    f.acct_num
ORDER BY
    f.acct_num;
