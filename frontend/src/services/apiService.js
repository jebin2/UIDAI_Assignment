const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchPublicKey() {
  const res = await fetch(`${BASE_URL}/api/v1/keys/public`);
  if (!res.ok) throw new Error("Failed to fetch public key");
  return res.json();
}

export async function submitSecurePayload(encryptedData, partnerId) {
  const res = await fetch(`${BASE_URL}/api/v1/sandbox/secure-payload`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      encrypted_data: encryptedData,
      partner_id: partnerId,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data?.detail?.message ?? data?.message ?? "Something went wrong.");
  }

  return data;
}
