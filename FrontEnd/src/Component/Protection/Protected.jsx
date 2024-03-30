import { Navigate } from "react-router-dom";
import toast from 'react-hot-toast'
import { useUserStore } from "../../Store/Store";

const Protected = ({children}) => {
    const { isAuthenticated, loading } = useUserStore();

    // Return null while loading
    if (loading) {
        // You can show a loading spinner here if needed
        return null;
    }

    // Handle authentication status
    if (!isAuthenticated) {
        toast.error("You need to log in first");
        return <Navigate to="/login" replace />;
    } else {
        return children;
    }
}

export default Protected;
