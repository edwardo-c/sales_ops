CREATE OR ALTER PROCEDURE dbo.usp_StatusReportPivot
  @current_year  INT,
  @previous_year INT
AS
BEGIN
  SET NOCOUNT ON;

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
      s.amount
    FROM status_report_all_sales s
    INNER JOIN status_report_customers c
      ON c.acct_num = s.acct_num
  )
  SELECT
    f.acct_num,
    ISNULL(SUM(CASE WHEN invoice_year = @previous_year AND product_category='mounts' THEN amount END),0) AS previous_year_mounts,
    ISNULL(SUM(CASE WHEN invoice_year = @previous_year AND product_category='tech'   THEN amount END),0) AS previous_year_tech,
    ISNULL(SUM(CASE WHEN invoice_year = @previous_year AND product_category='kiosks' THEN amount END),0) AS previous_year_kiosks,
    ISNULL(SUM(CASE WHEN invoice_year = @previous_year AND product_category='dvled'  THEN amount END),0) AS previous_year_dvled,
    ISNULL(SUM(CASE WHEN invoice_year = @current_year  AND product_category='mounts' THEN amount END),0) AS current_year_mounts,
    ISNULL(SUM(CASE WHEN invoice_year = @current_year  AND product_category='tech'   THEN amount END),0) AS current_year_tech,
    ISNULL(SUM(CASE WHEN invoice_year = @current_year  AND product_category='kiosks' THEN amount END),0) AS current_year_kiosks,
    ISNULL(SUM(CASE WHEN invoice_year = @current_year  AND product_category='dvled'  THEN amount END),0) AS current_year_dvled
  FROM filtered f
  GROUP BY f.acct_num
  ORDER BY f.acct_num;
END
