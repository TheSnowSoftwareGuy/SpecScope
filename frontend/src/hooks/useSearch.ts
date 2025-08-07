import React from "react";
import { api } from "../services/api";
import { SearchResult, QAResponse } from "../types";

const Ctx = React.createContext<any>(null);

export const SearchProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [query, setQuery] = React.useState("");
  const [alpha, setAlpha] = React.useState(0.5);
  const [results, setResults] = React.useState<SearchResult[]>([]);
  const [qa, setQa] = React.useState<QAResponse | null>(null);

  const runSearch = async () => {
    const res = await api.search({ query, top_k: 10, alpha });
    setResults(res);
  };
  const runQA = async () => {
    const res = await api.qa({ question: query, top_k: 12 });
    setQa(res);
  };

  return <Ctx.Provider value={{ query, setQuery, alpha, setAlpha, results, runSearch, qa, runQA }}>{children}</Ctx.Provider>;
};

export const useSearch = () => React.useContext(Ctx);