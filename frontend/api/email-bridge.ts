import { VercelRequest, VercelResponse } from '@vercel/node';
import nodemailer from 'nodemailer';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // 1. CORS headers (Optional but good)
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { to, subject, html, apiKey } = req.body;

  if (!apiKey || apiKey !== process.env.EMAIL_API_KEY) {
    console.error('[EMAIL PROXY] Unauthorized attempt with key:', apiKey);
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!to || !subject || !html) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
    },
  });

  try {
    console.log(`[EMAIL PROXY] Sending email to: ${to}`);
    await transporter.sendMail({
      from: process.env.SMTP_FROM_EMAIL || process.env.SMTP_USER,
      to,
      subject,
      html,
    });
    return res.status(200).json({ success: true, message: 'Email sent successfully' });
  } catch (error: any) {
    console.error('[EMAIL PROXY] Error:', error);
    return res.status(500).json({ success: false, error: error.message });
  }
}
