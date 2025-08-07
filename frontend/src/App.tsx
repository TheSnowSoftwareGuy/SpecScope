import React from "react";
import { UploadZone } from "./components/UploadZone";
import { SearchBar } from "./components/SearchBar";
import { ResultsPanel } from "./components/ResultsPanel";

export default function App() {
  const [tab, setTab] = React.useState<"search" | "qa" | "conflicts">("search");
  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">SpecScope MVP</h1>
      <UploadZone />
      <div className="mt-6">
        <SearchBar onTabChange={setTab} />
        <ResultsPanel activeTab={tab} />
      </div>
    </div>
  );
}
