import React from "react";
import { Citation } from "../types";

export const SourceViewer: React.FC<{ citation: Citation }> = ({ citation }) => {
  return (
    <div className="border rounded p-3">
      <div className="text-sm text-gray-600">{citation.filename} — p.{citation.page_number} {citation.section && `— ${citation.section}`}</div>
      <div className="mt-2">
        <mark>{citation.quote}</mark>
      </div>
    </div>
  );
};