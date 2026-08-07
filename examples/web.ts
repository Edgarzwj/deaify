// Example: humanizing AI-flavored web/TS code (code-humanizer skill).

// ---------------- BEFORE (AI-sounding) ----------------
// The function fetches the user from the API and returns the user object
function getUserData(userId: string) {
  try {
    const data = fetchUser(userId);
    if (data.isValid === true) {
      return data;
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
}

if (data && data.user && data.user.profile && data.user.profile.id) {
  const ms = 86400000;
  schedule(data.user.profile.id, ms);
}

// ---------------- AFTER (humanized) ----------------
function getUser(userId: string): User | undefined {
  try {
    const user = fetchUser(userId);
    return user.isValid ? user : undefined;
  } catch (error) {
    console.error(`Failed to load user ${userId}:`, error);
    return undefined;
  }
}

const DAY_IN_MS = 86_400_000;
if (user?.profile?.id) {
  schedule(user.profile.id, DAY_IN_MS);
}
