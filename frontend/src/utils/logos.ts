const companyLogos: Record<string, string> = {
  digitalocean: "/logos/digitalocean.svg",
  atlassian: "/logos/atlassian.svg",
  plaid_light: "/logos/plaid-light.svg",
  plaid_dark: "/logos/plaid-dark.svg",
  stripe: "/logos/stripe.svg",
  visa_light: "/logos/visa-light.svg",
  visa_dark: "/logos/visa-dark.svg",
  datadog_light: "/logos/datadog-light.svg",
  datadog_dark: "/logos/datadog-dark.svg",
  databricks_light: "/logos/databricks-light.svg",
  databricks_dark: "/logos/databricks-dark.svg",
};

export const getCompanyLogo = (company: string, darkMode: boolean) => {
  const normalized = company.toLowerCase();
  if (normalized === "databricks") return darkMode ? companyLogos.databricks_dark : companyLogos.databricks_light;
  if (normalized === "datadog") return darkMode ? companyLogos.datadog_dark : companyLogos.datadog_light;
  if (normalized === "plaid") return darkMode ? companyLogos.plaid_dark : companyLogos.plaid_light;
  if (normalized === "visa") return darkMode ? companyLogos.visa_dark : companyLogos.visa_light;
  return companyLogos[normalized] || "/logos/default.svg";
};
