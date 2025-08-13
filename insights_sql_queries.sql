-- Insight 1: Distribution of Ad Platforms
SELECT
    ad_platform,
    COUNT(ad_id) AS ad_count
FROM
    ads
GROUP BY
    ad_platform
ORDER BY
    ad_count DESC;

-- Insight 2: Distribution of Ad Types
SELECT
    ad_type,
    COUNT(ad_id) AS ad_count
FROM
    ads
GROUP BY
    ad_type
ORDER BY
    ad_count DESC;

-- Insight 3: Gender Distribution of Users
SELECT
    user_gender,
    COUNT(user_id) AS user_count
FROM
    users
GROUP BY
    user_gender
ORDER BY
    user_count DESC;

-- Insight 4: Age Group Distribution of Users
SELECT
    age_group,
    COUNT(user_id) AS user_count
FROM
    users
GROUP BY
    age_group
ORDER BY
    user_count DESC;

-- Insight 5: Top 5 Countries by User Count
SELECT
    country,
    COUNT(user_id) AS user_count
FROM
    users
GROUP BY
    country
ORDER BY
    user_count DESC
LIMIT 5;

-- Insight 6: Impressions by Ad Platform
SELECT
    a.ad_platform,
    COUNT(ae.event_id) AS impressions_count
FROM
    ad_events ae
JOIN
    ads a ON ae.ad_id = a.ad_id
WHERE
    ae.event_type = 'Impression'
GROUP BY
    a.ad_platform
ORDER BY
    impressions_count DESC;

-- Insight 7: Clicks by Ad Type
SELECT
    a.ad_type,
    COUNT(ae.event_id) AS clicks_count
FROM
    ad_events ae
JOIN
    ads a ON ae.ad_id = a.ad_id
WHERE
    ae.event_type = 'Click'
GROUP BY
    a.ad_type
ORDER BY
    clicks_count DESC;

-- Insight 8: CTR by Ad Platform
SELECT
    platform_impressions.ad_platform,
    CAST(COALESCE(platform_clicks.clicks_count, 0) AS REAL) / platform_impressions.impressions_count AS ctr
FROM
    (SELECT a.ad_platform, COUNT(ae.event_id) AS impressions_count
     FROM ad_events ae JOIN ads a ON ae.ad_id = a.ad_id
     WHERE ae.event_type = 'Impression' GROUP BY a.ad_platform) AS platform_impressions
LEFT JOIN
    (SELECT a.ad_platform, COUNT(ae.event_id) AS clicks_count
     FROM ad_events ae JOIN ads a ON ae.ad_id = a.ad_id
     WHERE ae.event_type = 'Click' GROUP BY a.ad_platform) AS platform_clicks
ON
    platform_impressions.ad_platform = platform_clicks.ad_platform
ORDER BY
    ctr DESC;

-- Insight 9: Conversion Rate (Purchase) by Ad Type
SELECT
    type_clicks.ad_type,
    CAST(COALESCE(type_purchases.purchases_count, 0) AS REAL) / type_clicks.clicks_count AS conversion_rate
FROM
    (SELECT a.ad_type, COUNT(ae.event_id) AS clicks_count
     FROM ad_events ae JOIN ads a ON ae.ad_id = a.ad_id
     WHERE ae.event_type = 'Click' GROUP BY a.ad_type) AS type_clicks
LEFT JOIN
    (SELECT a.ad_type, COUNT(ae.event_id) AS purchases_count
     FROM ad_events ae JOIN ads a ON ae.ad_id = a.ad_id
     WHERE ae.event_type = 'Purchase' GROUP BY a.ad_type) AS type_purchases
ON
    type_clicks.ad_type = type_purchases.ad_type
ORDER BY
    conversion_rate DESC;

-- Insight 10: Campaign Performance (Total Budget vs. Total Clicks)
SELECT
    c.campaign_id,
    c.total_budget,
    COALESCE(SUM(CASE WHEN ae.event_type = 'Click' THEN 1 ELSE 0 END), 0) AS total_clicks
FROM
    campaigns c
LEFT JOIN
    ads a ON c.campaign_id = a.campaign_id
LEFT JOIN
    ad_events ae ON a.ad_id = ae.ad_id
GROUP BY
    c.campaign_id, c.total_budget
ORDER BY
    c.campaign_id;
