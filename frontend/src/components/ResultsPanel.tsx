import React from "react";
import { useSearch } from "../hooks/useSearch";

export const ResultsPanel: React.FC<{ activeTab: "search" | "qa" | "conflicts" }> = ({ activeTab }) => {
  const { results, qa } = useSearch();
  if (activeTab === "search") {
    return (
      <div className="mt-4 space-y-3">
        {results.map(r => (
          <div key={r.chunk_id} className="border rounded p-3">
            <div className="text-sm text-gray-600">{r.filename} — p.{r.page_number} {r.section && `— ${r.section}`}</div>
            <div className="mt-1">{r.snippet}</div>
            <div className="text-xs mt-1">scores v:{r.scores.vector.toFixed(2)} k:{r.scores.keyword.toFixed(2)} h:{r.scores.hybrid.toFixed(2)} conf:{r.confidence.toFixed(2)}</div>
          </div>
        ))}
      </div>
    );
  }
  if (activeTab === "qa") {
    return (
      <div className="mt-4">
        <div className="font-medium">Answer</div>
        <div className="mt-1">{qa?.answer}</div>
        <div className="mt-2">
          <div className="font-medium">Citations</div>
          <ul className="list-disc pl-6">
            {qa?.citations?.map((c, i) => (
              <li key={i} className="text-sm">{c.filename} p.{c.page_number} — “{c.quote}”</li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
  return <div className="mt-4 text-sm text-gray-600">Conflicts view will appear here.</div>;
};
