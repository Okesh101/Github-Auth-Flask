import { useEffect, useState } from "react";
import apiFetch from "./api/client";
import "./Dashboard.css"

const AdminDashboard = () => {
  const [user, setUser] = useState(null);
  const [userData, setUserData] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await apiFetch("/api/v1/admin/dashboard");
        const data = await res.json();

        if (data.status === "SUCCESS") {
          setUser(data.data);
        } else {
          console.error("Failed to fetch user details:", data.message);
        }
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    };
    fetchUser();
  }, []);

  const handleFetchUsers = async () => {
    try {
      const options = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      };
      const res = await apiFetch("/api/v1/admin/users", options);
      const data = await res.json();

      if (data.status === "SUCCESS") {
        setUserData(data.data);
      } else {
        console.error("Failed to fetch users:", data.message);
      }
    } catch (error) {
      console.error("Error during fetching users:", error);
    }
  };

  const handleLogout = async () => {
    try {
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      };
      const res = await apiFetch("/api/v1/auth/logout", options);
      const data = await res.json();

      if (data.status === "SUCCESS") {
        window.location.href = "/";
        localStorage.removeItem("access_token");
        setUser(null);
      } else {
        console.error("Failed to logout:", data.message);
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <>
      <section id="center">
        <div className="hero">
          <img
            src={user?.picture}
            className="base"
            width="170"
            height="179"
            alt="User Image Not Available"
          />
        </div>
        <div>
          <h1>Dashboard</h1>
          <p>
            Welcome {user ? `Back ${user.name.split(" ")[0]}` : "New User"}
            ! <br />
            This is your dashboard where you can view your profile information
            and manage your account settings.
          </p>
          <br />
          <p>
            <strong>Name:</strong>{" "}
            {user ? user.name : "User Name Not Available"} <br />
            <strong>Email:</strong>{" "}
            {user ? user.email : "User Email Not Available"}
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => handleLogout()}
        >
          Sign Out
        </button>
        <button
          type="button"
          className="counter"
          onClick={() => handleFetchUsers()}
        >
          Get Users
        </button>
        {userData &&
          userData.map((user, index) => (
            <table
              className="users-table"
              style={{
                marginTop: "20px",
                borderCollapse: "collapse",
                width: "100%",
                border: "1px solid #ddd",
              }}
            >
              <caption>Admin Users</caption>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Display Name</th>
                  <th>Provider</th>
                  <th>Joined At</th>
                </tr>
              </thead>
              <tbody>
                <tr key={index}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{user.display_name}</td>
                  <td>{user.provider}</td>
                  <td>{new Date(user.joined_at).toLocaleDateString()}</td>
                </tr>
              </tbody>
            </table>
          ))}
      </section>
    </>
  );
};

export default AdminDashboard;
