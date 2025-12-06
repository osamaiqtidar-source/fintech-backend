-- Add language column to company for translations
ALTER TABLE company
  ADD COLUMN IF NOT EXISTS language varchar DEFAULT 'en';
