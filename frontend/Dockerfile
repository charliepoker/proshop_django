# Use Node.js v16-alpine image as the base image for the builder stage, which is lightweight and suitable for production
FROM node:16-alpine AS builder

# Set the working directory inside the container to /app
WORKDIR /app 

# Copy only the package.json and package-lock.json files to the working directory to install dependencies first
# This helps in leveraging Docker’s cache to avoid reinstalling dependencies if package files haven't changed
COPY package*.json ./

# Install dependencies, using --legacy-peer-deps to avoid issues with peer dependencies in this setup
RUN npm install --legacy-peer-deps

# Copy all other files from the local directory to the working directory in the container
COPY . .


# Start a new stage to keep the final image lightweight by only including the built app
FROM node:16-alpine

# Set the working directory again in this final stage
WORKDIR /app 

# Copy the entire application from the builder stage into the current stage
COPY --from=builder /app .

# Expose port 3000 for the app to listen on, making it accessible outside the container
EXPOSE 3000

# Run the application, typically starting a development or production server depending on the app configuration
CMD [ "npm", "start" ]