-- LinguaMaster Sync Tables
-- Migration: 20260131000001
-- Description: Create user_vocab and user_media tables for cloud sync feature

-- ============================================================================
-- 1. User Vocab (vocabulary sync)
-- ============================================================================
create table if not exists public.user_vocab (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  word text not null,
  translation text,
  context_sentence text,
  source_video text,
  language text default 'en',
  -- SRS (Spaced Repetition System) fields
  next_review_at timestamptz,
  interval int default 0,
  easiness_factor numeric(4,2) default 2.5,
  repetitions int default 0,
  -- Timestamps
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Unique constraint: one word per user per language
create unique index if not exists idx_user_vocab_unique
  on public.user_vocab(user_id, word, language);

create index if not exists idx_user_vocab_user_id
  on public.user_vocab(user_id);

create index if not exists idx_user_vocab_next_review
  on public.user_vocab(user_id, next_review_at);

-- Update trigger
create trigger update_user_vocab_updated_at
  before update on public.user_vocab
  for each row execute function update_updated_at_column();

-- ============================================================================
-- 2. User Media (video sync - metadata only, not files)
-- ============================================================================
create table if not exists public.user_media (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  source_url text not null,
  title text,
  cover_image text,
  duration int default 0,
  language text default 'en',
  -- Timestamps
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Unique constraint: one URL per user
create unique index if not exists idx_user_media_unique
  on public.user_media(user_id, source_url);

create index if not exists idx_user_media_user_id
  on public.user_media(user_id);

-- Update trigger
create trigger update_user_media_updated_at
  before update on public.user_media
  for each row execute function update_updated_at_column();

-- ============================================================================
-- 3. Row Level Security (RLS) Policies
-- ============================================================================

-- Enable RLS
alter table public.user_vocab enable row level security;
alter table public.user_media enable row level security;

-- User Vocab: users can only access their own vocabulary
create policy "Users can view own vocab"
  on public.user_vocab for select
  using (auth.uid() = user_id);

create policy "Users can insert own vocab"
  on public.user_vocab for insert
  with check (auth.uid() = user_id);

create policy "Users can update own vocab"
  on public.user_vocab for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can delete own vocab"
  on public.user_vocab for delete
  using (auth.uid() = user_id);

-- User Media: users can only access their own media
create policy "Users can view own media"
  on public.user_media for select
  using (auth.uid() = user_id);

create policy "Users can insert own media"
  on public.user_media for insert
  with check (auth.uid() = user_id);

create policy "Users can update own media"
  on public.user_media for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can delete own media"
  on public.user_media for delete
  using (auth.uid() = user_id);

-- ============================================================================
-- 4. Comments
-- ============================================================================
comment on table public.user_vocab is 'User vocabulary for cloud sync with SRS data';
comment on table public.user_media is 'User video metadata for cloud sync (URLs only, no files)';
