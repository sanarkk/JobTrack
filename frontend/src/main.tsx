import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App/App.tsx'
import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {Toaster} from "react-hot-toast";
import DashboardPage from "./pages/DashboardPage/DashboardPage.tsx";
import SavedJobsPage from "./pages/SavedJobsPage/SavedJobsPage.tsx";
import ResumePage from "./pages/ResumePage/ResumePage.tsx";
import AiAssistantPage from "./pages/AiAssistantPage/AiAssistantPage.tsx";



createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <BrowserRouter>
            <Toaster
                position="top-center"
                gutter={8}
                containerClassName=""
                containerStyle={{}}
                toastOptions={{
                    className: "",
                    style: {
                        background: "#363636",
                        color: "#fff",
                    },
                    success: {
                        duration: 3000,
                    },
                }}
            />
            <Routes>
                <Route path="/" element={<App/>}>
                    <Route index element={<Navigate to="dashboard" replace />} />
                    <Route path="dashboard" element={<DashboardPage/>} />
                    <Route path="resume" element={<ResumePage/>} />
                    <Route path="saved" element={<SavedJobsPage/>} />
                    <Route path="ai-assistant" element={<AiAssistantPage/>} />
                </Route>
            </Routes>
        </BrowserRouter>
    </StrictMode>,
)
