import React from "react";
import { useSearch } from "../hooks/useSearch";

export const SearchBar: React.FC<{ onTabChange?: (t: "search" | "qa" | "conflicts") => void }> = ({ onTabChange }) => {
  const { query, setQuery, alpha, setAlpha, runSearch, runQA } = useSearch();
  return (
    <div className="flex items-center gap-2">
      <input className="border p-2 flex-1" placeholder="Search specs..." value={query} onChange={(e) => setQuery(e.target.value)} />
      <label className="text-sm">alpha {alpha.toFixed(2)}</label>
      <input type="range" min={0} max={1} step={0.05} value={alpha} onChange={(e) => setAlpha(parseFloat(e.target.value))} />
      <button className="px-3 py-1 bg-gray-200 rounded" onClick={() => { runSearch(); onTabChange?.("search"); }}>Search</button>
      <button className="px-3 py-1 bg-green-600 text-white rounded" onClick={() => { runQA(); onTabChange?.("qa"); }}>Ask</button>
    </div>
  );
};