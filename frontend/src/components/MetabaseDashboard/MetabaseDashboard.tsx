import { useEffect, useRef } from "react";

interface MetabaseDashboardProps {
    token: string;
    dashboardId: number;
}

const MetabaseDashboard = ({ token, dashboardId }: MetabaseDashboardProps) => {
    const containerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (!token) return;

        // Clear previous dashboard
        if (containerRef.current) {
            containerRef.current.innerHTML = "";
        }

        // Define Metabase config globally
        (window as any).metabaseConfig = {
            theme: { preset: "light" },
            isGuest: true,
            instanceUrl: "http://localhost:3000",
        };

        // Create dashboard element
        if (containerRef.current) {
            const dash = document.createElement("metabase-dashboard");
            dash.setAttribute("token", token);
            dash.setAttribute("with-title", "true");
            dash.setAttribute("with-downloads", "true");
            containerRef.current.appendChild(dash);
        }

        // Load script only once
        const existingScript = document.querySelector(`script[src="http://localhost:3000/app/embed.js"]`);
        if (!existingScript) {
            const script = document.createElement("script");
            script.src = "http://localhost:3000/app/embed.js";
            script.defer = true;
            document.body.appendChild(script);
        }
    }, [token, dashboardId]);

    return <div ref={containerRef} style={{ width: "100%", height: "100vh" }} />;
};

export default MetabaseDashboard;
