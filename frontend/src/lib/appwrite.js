import { Client, Account, Databases, ID } from "appwrite";

const projectId = import.meta.env.VITE_APPWRITE_PROJECT_ID;

const client = new Client()
  .setEndpoint(import.meta.env.VITE_APPWRITE_ENDPOINT || "https://nyc.cloud.appwrite.io/v1")
  .setProject(projectId || "");

export const account = new Account(client);
export const databases = new Databases(client);
export { ID };

export const DB_ID = import.meta.env.VITE_APPWRITE_DB_ID;
export const COLLECTION_ID = "audit_results";

export const isAppwriteConfigured = () =>
  Boolean(projectId && import.meta.env.VITE_APPWRITE_DB_ID);
