import { useEffect, useReducer, useRef } from "react";
import { fetchPublicKey, submitSecurePayload } from "../services/apiService";
import { encryptPayload, importPublicKey } from "../services/cryptoService";

const INITIAL_STATE = {
  fields: { name: "", aadhaarNumber: "", deviceId: "", partnerId: "" },
  status: "idle",
  transactionId: null,
  errorMessage: null,
};

function reducer(state, action) {
  switch (action.type) {
    case "SET_FIELD":
      return {
        ...state,
        fields: { ...state.fields, [action.name]: action.value },
        status: "idle",
        transactionId: null,
        errorMessage: null,
      };
    case "ENCRYPTING":
      return { ...state, status: "encrypting", transactionId: null, errorMessage: null };
    case "SUBMITTING":
      return { ...state, status: "submitting" };
    case "SUCCESS":
      return { ...state, status: "success", transactionId: action.transactionId };
    case "ERROR":
      return { ...state, status: "error", errorMessage: action.message };
    default:
      return state;
  }
}

export function useSecurePayload() {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);
  const cryptoKeyRef = useRef(null);

  useEffect(() => {
    async function preloadKey() {
      try {
        const { public_key } = await fetchPublicKey();
        cryptoKeyRef.current = await importPublicKey(public_key);
      } catch (err) { console.warn("Key preload failed:", err); }
    }
    preloadKey();
  }, []);

  function setField(name, value) {
    dispatch({ type: "SET_FIELD", name, value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    dispatch({ type: "ENCRYPTING" });

    let encryptedData;
    try {
      if (!cryptoKeyRef.current) {
        const { public_key } = await fetchPublicKey();
        cryptoKeyRef.current = await importPublicKey(public_key);
      }
      const identityPayload = JSON.stringify({
        name: state.fields.name.trim(),
        aadhaar_number: state.fields.aadhaarNumber.trim(),
        device_id: state.fields.deviceId.trim(),
      });
      encryptedData = await encryptPayload(cryptoKeyRef.current, identityPayload);
    } catch (err) {
      dispatch({ type: "ERROR", message: err.message });
      return;
    }

    dispatch({ type: "SUBMITTING" });

    try {
      const response = await submitSecurePayload(encryptedData, state.fields.partnerId.trim());
      dispatch({ type: "SUCCESS", transactionId: response.transaction_id });
    } catch (err) {
      dispatch({ type: "ERROR", message: err.message });
    }
  }

  return { state, setField, handleSubmit };
}
