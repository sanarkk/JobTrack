import { useEffect, useState } from "react";
import MetabaseDashboard from "../../components/MetabaseDashboard/MetabaseDashboard";

const StatsPage = () => {
    const [token, setToken] = useState<string | null>(null);
    const dashboardId = 123; // your dashboard id

    useEffect(() => {
        const fetchToken = async () => {
            try {
                const res = await fetch("http://0.0.0.0:8001/generate_metabase_token/", {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
                    },
                });
                const data = await res.json();
                setToken(data.token);
            } catch (error) {
                console.error("Failed to fetch Metabase token:", error);
            }
        };

        fetchToken();
    }, []);

    if (!token) return <div>Loading dashboard...</div>;

    return <MetabaseDashboard token={token} dashboardId={dashboardId} />;
};

export default StatsPage;
