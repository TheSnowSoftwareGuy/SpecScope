import React from "react";
import { api } from "../services/api";

export const ExportButton: React.FC<{ type: "csv" | "pdf" }> = ({ type }) => {
  const onExport = async () => {
    const blob = await api.export(type);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `specscope.${type}`;
    a.click();
    URL.revokeObjectURL(url);
  };
  return <button className="px-3 py-1 bg-indigo-600 text-white rounded" onClick={onExport}>Export {type.toUpperCase()}</button>;
};