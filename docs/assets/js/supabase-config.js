// =============================================================================
// Supabase config — public values, safe to commit.
// RLS policies on the `events` table protect the data itself:
//   - anon key can INSERT (records events from the public site)
//   - only the authenticated owner can SELECT (dashboard reads)
// =============================================================================
window.SUPABASE_URL = "https://bickwphtgbjsydlwowov.supabase.co";
window.SUPABASE_KEY = "sb_publishable_q_s8ltWC1rmHEduROyYZTA_bX7viGJS";
window.OWNER_EMAIL  = "weimingwong78@gmail.com";
