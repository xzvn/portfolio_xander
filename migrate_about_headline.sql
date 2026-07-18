ALTER TABLE profiles
ADD COLUMN about_headline VARCHAR(180) NULL;

UPDATE profiles
SET about_headline =
    'Mengenal saya dan perjalanan yang sedang saya bangun.'
WHERE about_headline IS NULL
   OR TRIM(about_headline) = '';
