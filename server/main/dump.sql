PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE IF NOT EXISTS "comment" (
	"commentId" VARCHAR(255) NOT NULL, 
	"postIdRef" VARCHAR(255) NOT NULL, 
	"commentContent" TEXT NOT NULL, 
	"createdDate" DATETIME NOT NULL, 
	"updatedDate" DATETIME NOT NULL, 
	"writerUid" VARCHAR(255) NOT NULL, 
	PRIMARY KEY ("commentId", "postIdRef"), 
	UNIQUE ("commentId")
);
CREATE TABLE IF NOT EXISTS "post" (
	"postId" VARCHAR(255) NOT NULL, 
	"writerUid" VARCHAR(255) NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	content TEXT NOT NULL, 
	"postViewCount" INTEGER NOT NULL, 
	"createdDate" DATETIME NOT NULL, 
	"updatedDate" DATETIME NOT NULL, 
	category VARCHAR(255) NOT NULL, 
	"imageUrl" VARCHAR(255), 
	PRIMARY KEY ("postId", "writerUid")
);
CREATE TABLE IF NOT EXISTS "user" (
	uid VARCHAR(255) NOT NULL, 
	PRIMARY KEY (uid)
);
COMMIT;
