import axios from "axios";
import { config } from "../config/env";

export const sendMessage = (message) => {
  const user_id =
    localStorage.getItem("email") || "guest";

  return axios.post("http://localhost:8000/chat", {
    message,
    user_id
  });
};