import {
  databases,
  ID,
  DB_ID,
  COLLECTION_ID,
  isAppwriteConfigured,
} from "./appwrite";

export async function saveAuditResult(biasReport, modelName, attribute) {
  if (!isAppwriteConfigured()) {
    console.warn("Appwrite env vars missing - skipping audit save.");
    return null;
  }
  return databases.createDocument(DB_ID, COLLECTION_ID, ID.unique(), {
    model: modelName,
    attribute,
    bias_level: biasReport.bias_level,
    disparity: biasReport.disparity,
    disadvantaged_group: biasReport.disadvantaged_group,
    timestamp: new Date().toISOString(),
  });
}

export async function listAuditResults(limit = 25) {
  if (!isAppwriteConfigured()) return [];
  const res = await databases.listDocuments(DB_ID, COLLECTION_ID);
  return (res.documents || []).slice(0, limit);
}
