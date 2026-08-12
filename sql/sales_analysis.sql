-- 1. Vue d'ensemble : Chiffre d'affaires et quantité totale par catégorie de produits
SELECT 
    p.category_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS total_units_sold,
    ROUND(SUM(s.sales_amount), 2) AS total_revenue,
    ROUND(AVG(s.sales_amount), 2) AS avg_order_value
FROM 
    sales_transactions s
JOIN 
    products p ON s.product_id = p.product_id
GROUP BY 
    p.category_name
ORDER BY 
    total_revenue DESC;

-- 2. Analyse temporelle et Croissance Mensuelle (MoM Growth) avec fonction de fenêtrage
WITH MonthlySales AS (
    SELECT 
        DATE_TRUNC('month', s.order_date) AS sales_month,
        SUM(s.sales_amount) AS current_month_revenue
    FROM 
        sales_transactions s
    GROUP BY 
        DATE_TRUNC('month', s.order_date)
)
SELECT 
    sales_month,
    current_month_revenue,
    LAG(current_month_revenue, 1) OVER (ORDER BY sales_month) AS previous_month_revenue,
    ROUND(
        (current_month_revenue - LAG(current_month_revenue, 1) OVER (ORDER BY sales_month)) 
        / NULLIF(LAG(current_month_revenue, 1) OVER (ORDER BY sales_month), 0) * 100, 2
    ) AS mom_growth_percentage
FROM 
    MonthlySales
ORDER BY 
    sales_month;
