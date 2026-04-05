import { useSecurePayload } from "../hooks/useSecurePayload";
import Field from "./Field";
import "../styles/SecurePayloadForm.css";

function allFilled(fields) {
  return Object.values(fields).every((v) => v.trim().length > 0);
}

function statusLabel(status) {
  if (status === "encrypting") return "Encrypting…";
  if (status === "submitting") return "Submitting…";
  return "Submit Securely";
}

export default function SecurePayloadForm() {
  const { state, setField, handleSubmit } = useSecurePayload();
  const { fields, status, transactionId, errorMessage } = state;
  const isLoading = status === "encrypting" || status === "submitting";

  return (
    <div className="card">
      <h2>Secure Identity Payload Simulator</h2>
      <p>Data is encrypted on your device before transmission using RSA-OAEP.</p>

      <form className="form" onSubmit={handleSubmit} noValidate>
        <Field label="Full Name" name="name" value={fields.name}
          placeholder="Jebin Einstein E" disabled={isLoading}
          onChange={(v) => setField("name", v)} />

        <Field label="Mock Aadhaar Number" name="aadhaarNumber" value={fields.aadhaarNumber}
          placeholder="XXXX-XXXX-1234" disabled={isLoading}
          onChange={(v) => setField("aadhaarNumber", v)} />

        <Field label="Device ID" name="deviceId" value={fields.deviceId}
          placeholder="device-abc-001" disabled={isLoading}
          onChange={(v) => setField("deviceId", v)} />

        <Field label="Partner ID" name="partnerId" value={fields.partnerId}
          placeholder="partner-001" disabled={isLoading}
          onChange={(v) => setField("partnerId", v)} />

        <div className="btn-wrapper">
          <button className="btn" type="submit" disabled={isLoading || !allFilled(fields)}>
            {statusLabel(status)}
          </button>

          {(status === "success" || status === "error") && (
            <div className={`feedback-overlay ${status}`}>
              {status === "success" && <>Payload accepted. Transaction ID: <strong>{transactionId}</strong></>}
              {status === "error" && errorMessage}
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
