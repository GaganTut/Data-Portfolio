with events as (
    select * from {{ ref('stg_events') }}
),

daily_summary as (
    select
        DATE(event_at) as metric_date,
        device,
        count(distinct user_id) as daily_active_users,
        count(event_id) as total_events
        
    from events
    group by 1, 2
)

select * from daily_summary