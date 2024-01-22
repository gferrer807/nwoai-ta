## **Schema Design**

The ETL pipeline's data architecture leverages a design closely aligned with the Star Schema concept, particularly in how data is segmented into collections within MongoDB. This approach mirrors the traditional star schema's structure by having a central fact table (posts collection) and related dimension tables (authors, subreddits, and media collections), linked via Object IDs.

Normally I might implement a non-normalized schema for NoSQL but the star schema gives some flexibility in incorporating more relation structures and relationships.

## **Improved Testing**

I would improve the testing suite to have more comprehensive coverage but for the sake of time and simplicity, I've left the test coverage to be small and light

## **Pub/Sub for Local Testing**

The initial plan was to use the local Pub/Sub emulator for testing to closely mimic the production environment. However, due to challenges encountered, this was set aside. Moving forward, integrating the Pub/Sub emulator remains a priority to ensure that local development and testing environments accurately reflect production settings, reducing the risk of environment-specific bugs and issues.

## **Deploy Scripts**

To streamline the deployment process and enhance reliability:

- **Automation:** Implementing Jenkins pipelines to automate deploy scripts for changes detected in main, staging, or production branches can significantly improve deployment efficiency.
- **Version Control:** Automated scripts help maintain a clear version history of what's deployed, facilitating easier rollback and tracking of changes.
- **Error Reduction:** Automation reduces the risk of human error in the deployment process, ensuring that only validated and approved code is deployed to production environments.