import React from "react";
import { api } from "../services/api";

export const useDocuments = () => {
  const [docs, setDocs] = React.useState<any[]>([]);
  const refresh = async () => {
    setDocs(await api.documents());
  };
  React.useEffect(() => { refresh(); }, []);
  return { docs, refresh };
};