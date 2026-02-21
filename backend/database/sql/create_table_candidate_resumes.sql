-- candidate_resumes table

create table if not exists public.candidate_resumes (
  id uuid primary key default gen_random_uuid(),

  -- optional: link to auth.users if you want per-user storage
  user_id uuid null references auth.users(id) on delete set null,

  -- source fields (duplicated for easy filtering)
  file_name text not null,
  file_path text null,
  extension text null,

  -- profile fields (duplicated for easy querying)
  profile_name text null,
  email text null,
  mobile_number text null,
  designation text null,
  total_experience text null,
  education text null,

  -- arrays (queryable with GIN index)
  skills text[] not null default '{}'::text[],
  company_names text[] not null default '{}'::text[],

  -- summary
  ai_summary text null,
  ai_strengths text[] not null default '{}'::text[],

  -- experiences: keep structured (array of objects)
  experiences jsonb not null default '[]'::jsonb,

  -- the full original object (source of truth)
  resume_json jsonb not null,

  -- housekeeping
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
