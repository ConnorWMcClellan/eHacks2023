const {MongoClient} = require('mongodb');

async function main()
{
    const link = "mongodb+srv://UmbranDrake:eHacks23FlyinLions@atscluster.cez6evd.mongodb.net/?retryWrites=true&w=majority";

    const client = new MongoClient(link);
    
    try
    {
        await client.connect();
        await listDatabases(client);
        await listCollections(client);
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

async function listCollections(client)
{
    //C. McCellen's attempt
    //const db = client.db('ats');
    //const collections = await db.listCollections().toArray();
    //console.log(collections[2])
    //if(collections[2].name === 'records')
    //{
    //   const data = db.collection('records');
    //   const cursor = data.find({})

    //   console.log(cursor);
    //}

    const database = client.db("ats");
    const col = database.collection("records");
    let searchptr = await col.find({});
    let result = await searchptr.toArray();
    console.table(result);

}