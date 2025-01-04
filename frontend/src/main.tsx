import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import "./index.css";
import AdminPage from "./pages/AdminPage.tsx";
import ListingsPage from "./pages/ListingsPage.tsx";

const root = document.getElementById("root")!;
createRoot(root).render(
    <StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<ListingsPage />} />
                <Route path="/admin" element={<AdminPage />} />
            </Routes>
        </BrowserRouter>
    </StrictMode>
);
