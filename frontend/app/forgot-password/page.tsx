"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

import { ApiClientError, apiClient } from "@/lib/api-client";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      const result = await apiClient.forgotPassword(email);
      setMessage(result.message);
    } catch (err) {
      setMessage(err instanceof ApiClientError ? err.message : "Request failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6">
      <form onSubmit={onSubmit} className="w-full max-w-md space-y-4">
        <h1 className="text-center text-3xl font-bold">Forgot password</h1>
        <p className="text-center text-sm text-muted-foreground">
          Enter your email and we&apos;ll send a reset link if an account exists.
        </p>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="w-full rounded border border-input bg-background px-3 py-2"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-foreground px-3 py-2 text-background disabled:opacity-60"
        >
          {loading ? "Sending…" : "Send reset link"}
        </button>
        {message && <p className="text-center text-sm text-muted-foreground">{message}</p>}
        <Link href="/login" className="block text-center text-sm underline">
          Back to login
        </Link>
      </form>
    </main>
  );
}
