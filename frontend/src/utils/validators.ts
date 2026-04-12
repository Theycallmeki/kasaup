/**
 * Shared form validation utilities for KasaUp
 */

/** PH phone: +63 followed by 10 digits (9xxxxxxxxx), spaces/dashes allowed */
const PH_PHONE_RE = /^\+63[\s-]?9\d{2}[\s-]?\d{3}[\s-]?\d{4}$/

/** Basic email regex */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export const validateEmail = (email: string): string | null => {
  if (!email.trim()) return 'Email is required.'
  if (!EMAIL_RE.test(email.trim())) return 'Please enter a valid email address.'
  return null
}

/**
 * Validates a Philippine mobile number.
 * Accepts: +639XXXXXXXXX, +63 9XX XXX XXXX, 09XXXXXXXXX (auto-converts)
 * Returns the normalized +63 form, or null if invalid.
 */
export const normalizePHPhone = (raw: string): string | null => {
  const stripped = raw.replace(/[\s\-()]/g, '')

  // Already in +63 format
  if (/^\+639\d{9}$/.test(stripped)) return stripped

  // Starts with 09 → convert to +63
  if (/^09\d{9}$/.test(stripped)) return '+63' + stripped.slice(1)

  // Starts with 639 (no +) → add +
  if (/^639\d{9}$/.test(stripped)) return '+' + stripped

  return null
}

export const validatePHPhone = (phone: string): string | null => {
  if (!phone.trim()) return null // phone is optional in most forms
  const normalized = normalizePHPhone(phone.trim())
  if (!normalized) {
    return 'Phone must be a valid PH number (e.g. +63 912 345 6789 or 09123456789).'
  }
  return null
}

export const validatePHPhoneRequired = (phone: string): string | null => {
  if (!phone.trim()) return 'Phone number is required.'
  return validatePHPhone(phone)
}

export const validatePassword = (password: string): string | null => {
  if (!password) return 'Password is required.'
  if (password.length < 8) return 'Password must be at least 8 characters.'
  return null
}

export const validateFullName = (name: string): string | null => {
  if (!name.trim()) return 'Full name is required.'
  if (name.trim().length < 2) return 'Full name must be at least 2 characters.'
  return null
}

export const validateShopName = (name: string): string | null => {
  if (!name.trim()) return 'Shop name is required.'
  if (name.trim().length < 2) return 'Shop name must be at least 2 characters.'
  return null
}
