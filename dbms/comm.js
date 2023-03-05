const {MongoClient} = require('mongodb');

async function main()
{
    const link = "mongodb+srv://UmbranDrake:eHacks23FlyinLions@atscluster.cez6evd.mongodb.net/?retryWrites=true&w=majority";

    const client = new MongoClient(link);
    
    try
    {
        await client.connect();
        await listDatabases(client);
    }
    catch (e)
    {
        console.error(e);
    }
    finally
    {
        await client.close();
    }
}

main().catch(console.error);

async function listDatabases(client)
{
    const list = await client.db().admin().listDatabases();
    console.log("Databases:");

    list.databases.forEach(db => {console.log(`- ${db.name}`)})
}