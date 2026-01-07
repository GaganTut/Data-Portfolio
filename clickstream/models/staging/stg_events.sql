with source as (
    select * from {{ source('clickstream_raw', 'events') }}
),

cleaned as (
    select
        event_id,
        user_id,
        event_name,
        device,
        client_timestamp,
        ip_address,

        CAST(client_timestamp AS TIMESTAMP) as event_at
    from source
)

select * from cleaned
where user_id is not null